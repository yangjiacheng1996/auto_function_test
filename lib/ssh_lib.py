#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import time
import paramiko


class SshCommandLine:
    def __init__(self, ipaddr, username, password, port=22, connect_retry=3, connect_retry_interval=10):
        """
        功能: 向远程主机建立SSH连接，连接成功将保存client对象，尝试失败多次后抛出异常。
        """
        self.ipaddr = ipaddr
        self.username = username
        self.password = password
        self.port = port
        self.retry = connect_retry
        self.retry_interval = connect_retry_interval
        self.ssh_client = self._create_ssh_client()

    def get_cli_response(self, cmd, timeout=10, wait=1):
        try:
            logging.info(f"Executing command: {cmd}")
            stdin, stdout, stderr = self.ssh_client.exec_command(cmd, get_pty=True, timeout=timeout)
            exit_status = stdout.channel.recv_exit_status()
            if exit_status == 0:
                logging.info(f"Execute cmd success!")
                output = stdout.read().decode()
                time.sleep(wait)
                return output
            else:
                logging.info("Execute cmd failed, so here is stderr:")
                output = stderr.read().decode()
                time.sleep(wait)
                return output
        except Exception as e:
            logging.error(e)
            raise Exception("Unknow error occurred!")

    def _create_ssh_client(self):
        while self.retry > 0:
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                ssh_client.connect(self.ipaddr, self.port, self.username, self.password,
                                   banner_timeout=30, auth_timeout=30, allow_agent=False)
                logging.info(f"SSH connect success: --> {self.ipaddr}")
                return ssh_client
            except Exception as e:
                logging.error(f"SSH connect failed: {e}, now try again...")
                time.sleep(self.retry_interval)
                self.retry -= 1
        raise Exception(f"SSH connect failed after retry {self.retry} times. Remote host {self.ipaddr} unreachable!")
