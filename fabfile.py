from fabric.api import local, env
import os
import shutil
import sys
import SimpleHTTPServer
import SocketServer

# Local path configuration (can be absolute or relative to fabfile)
env.project_dir = os.getcwd()
env.deploy_path = os.path.join(env.project_dir, 'output')
DEPLOY_PATH = env.deploy_path
env.pelican_config = os.path.join(env.project_dir, 'pelicanconf.py')

# Remote server configuration
# production = '$ssh_user@$ssh_host:$ssh_port'
# dest_path = '$ssh_target_dir'

# Rackspace Cloud Files configuration settings
# env.cloudfiles_username = '$cloudfiles_username'
# env.cloudfiles_api_key = '$cloudfiles_api_key'
# env.cloudfiles_container = '$cloudfiles_container'

# Github Pages configuration
env.github_pages_branch = "gh-pages"

# Port for `serve`
PORT = 8000

def clean():
    """Remove generated files"""
    if os.path.isdir(DEPLOY_PATH):
        shutil.rmtree(DEPLOY_PATH)
        os.makedirs(DEPLOY_PATH)

def build():
    """Build local version of site"""
    local('pelican -s ' + env.pelican_config)

def rebuild():
    """`clean` then `build`"""
    clean()
    build()

def regenerate():
    """Automatically regenerate site upon file modification"""
    import fabuild as fb
    fb.watch(build, os.path.join(env.project_dir, 'content'))

def serve():
    """Serve site at http://localhost:8000/"""
    os.chdir(env.deploy_path)

    class AddressReuseTCPServer(SocketServer.TCPServer):
        allow_reuse_address = True

    server = AddressReuseTCPServer(('', PORT), SimpleHTTPServer.SimpleHTTPRequestHandler)

    sys.stderr.write('Serving on port {0} ...\n'.format(PORT))
    server.serve_forever()

def reserve():
    """`build`, then `serve`"""
    build()
    serve()

def develop():
    """Runs `serve` and `regenerate` in parallel."""
    import fabuild as fb
    fb.build_run(serve, async=True)
    fb.build_run(regenerate)

def preview():
    """Build production version of site"""
    local('pelican -s publishconf.py')

# def cf_upload():
#     """Publish to Rackspace Cloud Files"""
#     rebuild()
#     with lcd(DEPLOY_PATH):
#         local('swift -v -A https://auth.api.rackspacecloud.com/v1.0 '
#               '-U {cloudfiles_username} '
#               '-K {cloudfiles_api_key} '
#               'upload -c {cloudfiles_container} .'.format(**env))

# @hosts(production)
# def publish():
#     """Publish to production via rsync"""
#     local('pelican -s publishconf.py')
#     project.rsync_project(
#         remote_dir=dest_path,
#         exclude=".DS_Store",
#         local_dir=DEPLOY_PATH.rstrip('/') + '/',
#         delete=True,
#         extra_opts='-c',
#     )

def gh_pages():
    """Publish to GitHub Pages"""
    rebuild()
    local("ghp-import -b {github_pages_branch} {deploy_path}".format(**env))
    local("git push origin {github_pages_branch}".format(**env))
