# coding=utf-8
__author__ = 'wan'

from email.mime.text import MIMEText
from email.utils import formataddr, parseaddr
from email import encoders
from email.header import Header
import smtplib





EMAIL_HOST = 'smtp.mxhichina.com'
EMAIL_PORT = 25    #ssl加密 465
EMAIL_USER = 'wmm@jiuyescm.com'
EMAIL_PASSWORD = 'wan355205045#'





def _format_addr(s):
    """
    不能简单地传入name <addr@example.com>，因为如果包含中文，需要通过Header对象进行编码
    :param s:
    :return:
    """
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr.encode('utf-8') if isinstance(addr, unicode) else addr))



def send_email(subject, content, to, type='html', code='utf=8'):
    """
    发送邮件
    :param subject:主题
    :param content:内容
    :param to:收件人,列表,但是在发送的时候需要转化成字符串
    :param type:邮件类型，是发送html还是文本(plain)
    :param code:编码
    :return:
    """

    if not subject or not content or not to:
        return False, '邮件主题或内容或联系人不能为空'

    if not isinstance(to, list):
        to = [to]

    try:
        msg = MIMEText(content, _subtype=type, _charset=code)
        msg['Subject'] = subject
        msg['From'] = _format_addr(u'九曳订单管理员<%s>' % EMAIL_USER)
        msg['To'] = ','.join(to)

        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.set_debuglevel(1)
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_USER, to, msg.as_string())
        server.quit()
        return True, '发送成功'

    except Exception, e:

        print e.message
        return False, '调用异常'




if __name__ == '__main__':
    success, msg = send_email('给王总的一封信(你的粉丝)', '我是一名资深程序员兼DOTA玩家,我擅长前端开发,游戏中,我拿手英雄有:UG,猴子,乐器,船长.大家都叫我王大帅', 'wangyong@jiuyescm.com', type='plain')
    print success
    print msg