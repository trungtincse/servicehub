from ckanext.servicehub.view import ServiceController, CallController, TestController,\
    ViewController, PackageController, ProjectController
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckanext.servicehub.auth.create as create_auth
import ckanext.servicehub.auth.show as show_auth
import ckanext.servicehub.action.create as create
import ckanext.servicehub.action.read as read
import ckanext.servicehub.action.delete as delete


class ServicehubPlugin(plugins.SingletonPlugin,toolkit.DefaultDatasetForm):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.IAuthFunctions)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IDatasetForm)
    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'servicehub')

    def get_blueprint(self):
        return [ServiceController.service,
                CallController.call_blueprint,
                TestController.test_blueprint,
                # AppServer.appserver_blueprint,
                ViewController.view_blueprint,
                PackageController.package_blueprint,
                ProjectController.project_blueprint
                ]

    def get_auth_functions(self):
        return {'service_create': create_auth.service_create,'package_show':show_auth.package_show}

    def get_actions(self):
        all_function = dict()
        all_function.update(read.public_functions)
        all_function.update(create.public_functions)
        all_function.update(delete.public_functions)
        return all_function

    def create_package_schema(self):
        # let's grab the default schema in our plugin
        schema = super(ServicehubPlugin, self).create_package_schema()
        # our custom field
        schema['owner_org']= [toolkit.get_validator(u'ignore_missing')]
        schema['private']= [toolkit.get_validator(u'ignore_missing'), toolkit.get_validator(u'boolean_validator')]
        return schema
    def update_package_schema(self):
        # let's grab the default schema in our plugin
        schema = super(ServicehubPlugin, self).update_package_schema()
        # our custom field
        schema['owner_org']= [toolkit.get_validator(u'ignore_missing')]
        schema['private']= [toolkit.get_validator(u'ignore_missing'), toolkit.get_validator(u'boolean_validator')]
        return schema
    def package_types(self):
        return [u'output']

    def is_fallback(self):
        return False
    def show_package_schema(self):
        # let's grab the default schema in our plugin
        schema = super(ServicehubPlugin, self).show_package_schema()
        # our custom field
        schema['owner_org']= [toolkit.get_validator(u'ignore_missing')]
        return schema
