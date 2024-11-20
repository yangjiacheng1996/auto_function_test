#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import time
import logging


def command(cmd, timeout=60):
    """执行命令cmd，返回命令输出的内容。
    如果超时将会抛出TimeoutError异常。
    cmd - 要执行的命令
    timeout - 最长等待时间，单位：秒
    return code must be 0
    """
    logging.debug(f"Running command: {cmd}")
    begin = time.time()
    try:
        # 将命令和参数分开传递
        result = subprocess.run(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout, text=True)
        if result.returncode == 0:
            logging.debug(f"Command output: {result.stdout.strip()}")
            return result.stdout.strip()
        else:
            logging.error(f"Command error: {result.stderr.strip()}")
            raise Exception(f"Run {cmd} error: {result.stderr.strip()}")
    except subprocess.TimeoutExpired:
        raise TimeoutError(f"Run {cmd} timeout")
    except Exception as e:
        logging.error(f"Error running command: {cmd}, error: {e}")
        raise
    finally:
        logging.debug(f"Command finished in {time.time() - begin:.2f} seconds")
