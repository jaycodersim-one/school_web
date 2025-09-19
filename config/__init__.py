# Ensure admin branding is applied when Django imports the config package
try:
	from . import admin  # noqa: F401
except Exception:
	# Avoid import-time errors if Django isn't fully configured yet
	pass

