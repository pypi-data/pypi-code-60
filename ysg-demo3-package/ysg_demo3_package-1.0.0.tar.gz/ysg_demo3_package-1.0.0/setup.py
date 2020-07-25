
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'ysg_demo3_package',
    version = '1.0.0',
    py_modules =['demo2'],
    auther = 'yinshaoge',
    auther_email = 'yinshaoge@126.com',
    url = 'https://github.com/',
	long_description=long_description,                      # 包的详细介绍(一般通过加载README.md)
    long_description_content_type="text/markdown",          # 和上条命令配合使用，声明加载的是markdown文件
    description = 'A simple printer of lists',
	packages=setuptools.find_packages(),
	classifiers=[                                           # 关于包的其他元数据(metadata)
        "Programming Language :: Python :: 3",              # 该软件包仅与Python3兼容
        "License :: OSI Approved :: MIT License",           # 根据MIT许可证开源
        "Operating System :: OS Independent",               # 与操作系统无关
    ],
)
