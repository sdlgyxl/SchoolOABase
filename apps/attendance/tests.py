from django.test import TestCase

# Create your tests here.
import logging
logging.basicConfig(
    filename='example.log',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s:%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)


logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')
logging.warning('And this, too 测试一下汉字')