# MyReusableCode

## config

加载配置文件

```shell
[section1]
key = value

[section2]
key = value
```

返回字典

## mysqlpool

mysql 连接池

## split_string

根据自定义字典划分字符串

```python
# word: word frequency
dict = {'china': 1, 'vip': 1}

'chinavip1' --> ['china', 'vip', '1']
```

## threadpool

线程池