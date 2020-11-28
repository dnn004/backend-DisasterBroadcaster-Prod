class FilePath:
  @staticmethod
  def post_upload(instance, filename):
    return "post/{0}/{1}".format(instance.id, filename)

  @staticmethod
  def news_upload(instance, filename):
    return "news/{}".format(instance.id)

  @staticmethod
  def avatar(user, filename):
    return "user/{}".format(user.id)
  