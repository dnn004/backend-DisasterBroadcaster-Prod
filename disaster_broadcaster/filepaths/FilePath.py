class FilePath:
  @staticmethod
  def post_upload(instance, filename):
    return "post/{}".format(instance.id)

  @staticmethod
  def news_upload(instance, filename):
    return "news/{}".format(instance.id)

  @staticmethod
  def avatar(user, filename):
    return "user/{}".format(user.id)
  