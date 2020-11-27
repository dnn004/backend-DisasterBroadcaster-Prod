class FilePath:
  @staticmethod
  def post_upload(instance, filename):
    return "post/{}".format(filename)

  @staticmethod
  def news_upload(instance, filename):
    return "news/{}".format(filename)

  @staticmethod
  def avatar(user, filename):
    return "user/{}".format(filename)
  