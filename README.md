# auto_function_test

#### 介绍
本项目是一个用于功能测试的自动化框架，本框架是基于pytest开发的一款数据驱动测试框架。可实现接口测试、命令行测试、web测试、UI测试等。

项目地址：https://gitee.com/yangjiacheng1996/auto_function_test
#### 软件架构
1. lib：通用函数库，具备高复用性，是对第三方Python库的封装，主要包括接口测试、命令行测试、web测试。
2. case：存放测试用例，每个函数对应一个测试用例，函数参数永远是\*\*kwargs，返回值多样。用例所在的文件名随意，可以是测试集的名称。
3. testplan: 测试计划，每个测试计划是一个yaml文件，包含case函数名，传参，期望结果与实际结果的比较，case之间的参数传递。
4. vars： 测试参数文件，文件格式目前仅支持yaml，可以同时使用多个参数文件，比如-v var1.yml,var2.yml。
5. tools：测试工具，包括测试报告生成器、浏览器驱动等。
5. results: 存放测试结果、日志、测试报告等。
6. main.py：主程序，接受进程参数，调用测试计划，执行测试用例。


#### 安装教程
1. 检查系统python版本，本项目要求使用python3.9及以上版本。检查命令：python -V
2. 克隆本项目到本地：git clone https://gitee.com/yangjiacheng1996/auto_function_test.git
3. 创建虚拟环境：cd auto_function_test && python -m venv venv
4. 安装依赖：pip install -r requirements.txt
5. 运行案例testplan：python main.py test -t sample_testplan.yml -v sample_var.yml
6. 产生测试报告：先下载allure软件到本项目的tools目录中，

下载地址是https://github.com/allure-framework/allure2/releases/download/2.22.4/allure-2.22.4.zip  。

解压后进入bin目录，执行命令allure generate <result目录的绝对路径> -o <测试报告输出文件夹> --clean

因为allure测试报告中的index.html直接通过浏览器打开会不显示数据，所以必须通过allure命令打开测试报告。命令如下：

allure open <测试报告输出文件夹>

#### 使用说明

1. 如何编写lib: 根据需求或用途来创建lib文件，文件命名最好以_lib结尾，例如：api_lib.py，lib中的函数需要具备高复用性。因为lib是对库的封装，所以请不要在lib中使用varpool。
2. 如何编写case: case函数的形参必须是\*\*kwargs，用于接受来自testplan的args传参，函数的开头需要预先定义变量接收传数，并提高函数可读性。
3. 如何编写testplan：请参考案例sample_testplan.yml，每个case可包含多个step，每个step的return会自动保存到varpool.ret中
4. 参数传递：测试所用的参数可以保存到vars目录中，通过命令-v将参数传递到varpool中。也可以在testplan中定义常量。
case与case之间的参数传递可以使用varpool，只需要from lib.varpool_lib import varpool即可获得内存中varpool对象。


