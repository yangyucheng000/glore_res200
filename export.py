# Copyright 2021 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""
##############export checkpoint file into air, onnx, mindir models#################
python export.py
"""
import argparse
import numpy as np

from mindspore import Tensor, load_checkpoint, load_param_into_net, export, context
import mindspore.common.dtype as ms

from src.config import config1 as config
from src.glore_resnet200 import glore_resnet200

parser = argparse.ArgumentParser(description='Classification')
parser.add_argument("--device_id", type=int, default=0, help="Device id")
parser.add_argument("--batch_size", type=int, default=1, help="batch size")
parser.add_argument("--file_name", type=str, default="glore_resnet200", help="output file name.")
parser.add_argument('--file_format', type=str, choices=["AIR", "ONNX", "MINDIR"], default='AIR', help='file format')
parser.add_argument("--device_target", type=str, choices=["Ascend", "GPU", "CPU"], default="Ascend",
                    help="device target")
parser.add_argument("--ckpt_path", type=str, default=None)

args = parser.parse_args()

context.set_context(mode=context.GRAPH_MODE, device_target=args.device_target)
if args.device_target == "Ascend":
    context.set_context(device_id=args.device_id)

if __name__ == '__main__':
    net = glore_resnet200(class_num=config.class_num)
    assert args.ckpt_path is not None, "arg.ckpt_path is None."
    param_dict = load_checkpoint(args.ckpt_path)
    load_param_into_net(net, param_dict)

    input_arr = Tensor(np.ones([args.batch_size, 3, 224, 224]), ms.float32)
    export(net, input_arr, file_name=args.file_name, file_format=args.file_format)
