class FilePath:
  @staticmethod
  def post_upload(instance, filename):
    return "post/{0}/{1}".format(instance.id, filename)

  @staticmethod
  def news_upload(instance, filename):
    return "news/{0}/{1}".format(instance.id, filename)

  @staticmethod
  def avatar(user, filename):
    return "user/{0}/{1}".format(user.id, filename)
  