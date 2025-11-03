sphinx = find_program('sphinx-build', required: true)

# Define directories
build_root = meson.project_build_root()
source_root = meson.project_source_root()
doctrees_dir = join_paths(build_root, 'sphinx_doctrees')
source_dir = join_paths(source_root, 'docs')
mandir = get_option('mandir')

# Define the build types (formats) we want to generate
build_formats = ['html', 'man']

# List to store all generated custom targets
all_doc_targets = []

foreach format : build_formats
	# Define output and install variables based on the format
	target_name = 'sphinx-' + format
	
	if format == 'html'
		# html pages go to share/doc/<application_id>/html/lang
		install_path = join_paths(datadir, 'doc', application_id, format)
		target_outputs = [format] # Output directory 'html'
	elif format == 'man'
		# man pages go to share/man/<lang>/man1
		install_path = join_paths(mandir, 'man1')
		target_outputs = [application_id + '.1']
	endif
	
	# Create the custom target
	current_target = custom_target(
		target_name,
		output: target_outputs,
		command: [
			sphinx,
			'-E',
			'-b', format,
			'-d', doctrees_dir,
			source_dir,
			join_paths('docs', format),
		],
		build_by_default: true,
	)
	# Add the newly created target to our list
	all_doc_targets += current_target
	meson.add_install_script('install_docs.py', join_paths(build_root, 'docs', format), install_path)
endforeach

# Optional alias to build all docs at once
alias_target('docs', all_doc_targets)
