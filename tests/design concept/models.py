class blog(models.Model):
	blog = models.CharField(max_length=20, unique=True)

class author(models.Model):
	author = models.CharField(max_length=50)

class post(models.Model):
	title = models.CharField(max_length=50)
	content = models.TextField(max_length = 1000, nullable=True, blankable=True)
	blog = models.ForeignKey(blog)
	author = models.ForeignKey(author)