from django.db import models
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save

# Create your models here.
class Post(models.Model):
	title = models.CharField(max_length=250)
	image = models.ImageField(upload_to="blog_images", null=True, blank=True)
	slug = models.SlugField(unique=True, null=True)
	content = models.TextField()
	updated = models.DateTimeField(auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("posts:detail", kwargs={"slug": self.slug})

	class Meta:
		ordering = ['-timestamp', '-updated']




# def create_slug(instance, new_slug=None):
# 	slug_title = slugify(instance.title)
# 	if new_slug is not None:
# 		slug_title = new_slug
# 	qs = Post.objects.filter(slug=slug_title)
# 	exists = qs.exists()
# 	if exists:
# 		new_slug = "%s-%s"%(slug_title, instance.id)
# 		return create_slug(instance, new_slug=new_slug)
# 	return slug_title

def post_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		slug = slugify(instance.title)
		qs = Post.objects.filter(slug=slug)
		exists = qs.exists()
		if exists:
			slug = "%s-%s"%(slug, instance.id)
		instance.slug = slug
		instance.save()

post_save.connect(post_receiver, sender=Post)