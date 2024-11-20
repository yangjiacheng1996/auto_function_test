#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import yaml


def read_yaml(yaml_path):
    print("load yaml start -------------------")
    # load yaml
    try:
        with open(yaml_path, "r", encoding='utf-8') as f:
            yaml_dict = yaml.safe_load(f)
            # print(yaml_dict)
            # yaml_dict_obj = dictToObj(yaml_dict)
            logging.info(f"加载yaml到内存成功，文件路径：{yaml_path}")
            return yaml_dict
    except Exception as e:
        logging.error(e)
        raise IOError("加载配置文件失败，你给的配置文件是乱码的，或者有语法错误")


def write_yaml(file_path, json_obj):
    logging.info("dump start --------------------")
    with open(file_path, "w", encoding="utf-8", ) as wf:
        yaml.safe_dump(json_obj, wf, default_flow_style=False, encoding='utf-8', allow_unicode=True)
        logging.info(f"新配置导入文件成功。导入文件路径：{file_path}")
    return None
