from ..models import (
	Project,
	ProjectCategory,
	ProjectSubCategory
)

from .meta import Service

from sqlalchemy.sql import func


class ProjectService(Service):


	def get_projects_treemap_json(self):
		# Header for google data
		tree_ar = [['Title', 'Parent', 'Amount', 'City']]
		
		# Total amount of all the projects
		global_total_amount = self.dbsession.query(func.sum(Project.amount_total)).scalar()
		tree_ar.append(['Global', None, float(global_total_amount), 0])
		
		# Adding project categories
		projectcategories = self.dbsession.query(ProjectCategory).all()
		for projectcategory in projectcategories:
			category_total_amount = self.dbsession.query(func.sum(Project.amount_total)) \
												.filter(Project.category_id==projectcategory.id) \
												.scalar()
			tree_ar.append([str(projectcategory.name), 'Global', float(category_total_amount), 0])
		
		cat_names = [cat.name for cat in projectcategories]

		# Adding project sub categories
		projectsubcategories = self.dbsession.query(ProjectSubCategory).all()
		for projectsubcategory in projectsubcategories:
			sub_category_total_amount = self.dbsession.query(func.sum(Project.amount_total)) \
												.filter(Project.subcategory_id==projectsubcategory.id) \
												.scalar()
			if projectsubcategory.name in cat_names:
				projectsubcategory.name = projectsubcategory.name + ' '
			tree_ar.append([str(projectsubcategory.name), str(projectsubcategory.category.name), float(sub_category_total_amount), 0])

		subcat_names = [subcat.name for subcat in projectsubcategories]

		# Adding projects
		projects = self.dbsession.query(Project).all()
		proj_names = [proj.name for proj in projects]
		for project in projects:
			if project.name in subcat_names \
			or project.name in cat_names \
			or proj_names.count(project.name) > 1:
				project.name = project.name + '-' + str(project.id)
			tree_ar.append([str(project.name), str(project.subcategory.name), float(project.amount_total), project.city.id])

		return tree_ar