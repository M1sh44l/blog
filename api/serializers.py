from rest_framework import serializers
from posts.models import Post

class PostListSerializer(serializers.ModelSerializer):
	detail = serializers.HyperlinkedIdentityField(
		view_name="api:detail",
		lookup_field="slug",
		lookup_url_kwarg="post_slug",
		)
	delete = serializers.HyperlinkedIdentityField(
		view_name="api:delete",
		lookup_field="slug",
		lookup_url_kwarg="post_slug",
		)
	update = serializers.HyperlinkedIdentityField(
		view_name="api:update",
		lookup_field="slug",
		lookup_url_kwarg="post_slug",
		)
	author = serializers.SerializerMethodField()
	class Meta:
		model = Post
		fields = ['title', 'author', 'slug', 'content', 'publish', 'detail', 'delete', 'update']

	def get_author(self, obj):
		return str(obj.author.username)

class PostDetailSerializer(serializers.ModelSerializer):
	author = serializers.SerializerMethodField()
	class Meta:
		model = Post
		fields = ['id', 'title', 'author', 'slug', 'content', 'publish', 'draft']

	def get_author(self, obj):
		return str(obj.author.username)

class PostCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = ['title', 'content', 'publish', 'draft']

