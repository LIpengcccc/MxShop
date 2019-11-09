# encoding: utf-8
"""
@author:lipeng
@time:2019/11/6  21:09
"""

client_id = "3317834272"


def get_auth_url():
    weibo_auth_url = "https://api.weibo.com/oauth2/authorize"
    redirect_uri = "http://127.0.0.1:8000/complete/weibo/"
    auth_url = weibo_auth_url + "?client_id={client_id}&redirect_uri={redirect_uri}".format(client_id=client_id,
                                                                                            redirect_uri=redirect_uri)
    print(auth_url)


def get_access_token(code="a4cfe9d1959149b665a9b1b0fe8e74e4"):
    access_token_url = "https://api.weibo.com/oauth2/access_token"
    import requests
    re_dict = requests.post(access_token_url, data={
        "client_id": "3317834272",
        "client_secret": "7d24b3503a0f17d581fbcb8a8369ddf2",
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://127.0.0.1:8000/complete/weibo/"
    })



def get_uer_info(access_token="", uid=""):
    """

    :param access_token:
    :type uid: object
    """
    use_url = "https://api.weibo.com/2/users/show.json?access_token={access_token}&uid={uid}".format(
        access_token=access_token, uid=uid)

    print(use_url)


if __name__ == "__main__":
    get_auth_url()
    get_access_token(code="a4cfe9d1959149b665a9b1b0fe8e74e4")
    get_uer_info(access_token="2.00Df6oFGAQSXcD6b6ca5bc72kZxyvD", uid="5582693717")
