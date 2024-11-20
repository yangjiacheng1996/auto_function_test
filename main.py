#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import shutil
import json

project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_dir)
sys.path.append(os.path.join(project_dir, "lib"))
from lib.varpool_lib import varpool
from lib.yaml_lib import read_yaml

import click
import pytest


@click.group()
def main():
    # 创建result目录用于保存
    result_dir = varpool.result_dir
    print(result_dir)
    if os.path.exists(result_dir):
        shutil.rmtree(result_dir)
    try:
        os.mkdir(result_dir)
    except:
        print("can't create results folder, please check...")
        sys.exit(1)


@click.command()
@click.option("-t", "--testplan", help=f"testplan file name in {project_dir}/testplan/\n", required=True,
              default="sample.yml")
@click.option("-v", "--vars",
              help=f"vars file name in {project_dir}/vars/\n , comma separated if multiple files\n",
              required=True, default="")
@click.option("-f", "--feature", help="this testing for which function?\n", required=True, default="Default")
@click.option("-s", "--story", help="this testing for which target?\n", required=True, default="Default")
def test(testplan,vars, feature, story):
    # load script parameters into varpool
    varpool.testplan_filename = testplan
    varpool.vars_filename = vars.split(",")
    varpool.feature = feature
    varpool.story = story
    testplan_filepath = os.path.join(varpool.testplan_dir, varpool.testplan_filename)
    # check all vars file exist and load them into varpool
    if vars:
        for var_file in varpool.vars_filename:
            var_filepath = os.path.join(varpool.vars_dir, var_file.strip())
            if not os.path.exists(var_filepath):
                print(f"vars file {var_file} not found in {varpool.vars_dir}!")
                sys.exit(1)
            varpool.update(read_yaml(var_filepath))
    # load testplan and check format
    tp = read_yaml(testplan_filepath)
    varpool_json = open(os.path.join(varpool.result_dir, "vars.json"), "w+", encoding="utf-8")
    case_json = open(os.path.join(varpool.result_dir, "case.json"), "w+", encoding="utf-8")
    json.dump(varpool, varpool_json)
    json.dump(tp, case_json)
    varpool_json.close()
    case_json.close()
    # Run test function which receive parameters.
    cmd_list = [f"--alluredir={varpool.result_dir}",
                "-o", "log_cli=True",
                "-o", "log_cli_level=INFO",
                "-o", "log_cli_date_format=%Y-%m-%d %H:%M:%S",
                "-o", "log_cli_format=%(asctime)s %(levelname)s %(message)s",
                "--capture=fd",
                "-v", os.path.join(varpool.lib_dir, "run_case.py")]
    pytest.main(cmd_list)
    # Following codes will teach you how to use allure.
    # You can change the logo in test report , if you cannot finish this , google it ! Lots of blogs!
    report_dir = os.path.join(varpool.result_dir, "report")
    wget_allure_command = "wget https://github.com/allure-framework/allure2/releases/download/2.22.4/allure-2.22.4.zip"
    allure_generate_cmd = f"allure generate {varpool.result_dir} -o {report_dir} --clean"
    allure_show_cmd = f"allure open {report_dir}"
    print(f"To download allure,run command:\n\t{wget_allure_command}")
    print(f"To generate report,install java then use command:\n\t{allure_generate_cmd}")
    print(f"To show report in browser,use command: \n\t{allure_show_cmd}")
    os.remove(os.path.join(varpool.result_dir, "case.json"))
    os.remove(os.path.join(varpool.result_dir, "vars.json"))


main.add_command(test)

if __name__ == "__main__":
    main()
