import locale
from ..models import (
	City,
	Project,
	ProjectCategory,
	ProjectSubCategory,
	State,
)

from .meta import Service

from sqlalchemy.sql import func


class ProjectService(Service):


	def get_projects_treemap_json(self):

		locale.setlocale(locale.LC_MONETARY, 'enn')

		# Header for google data
		tree_ar = [['Title', 'Parent', 'Amount', 'City']]
		
		amount_dict = {}

		# Total amount of all the projects
		global_total_amount = self.dbsession.query(func.sum(Project.amount_total)).scalar()
		amount_dict['Global'] = locale.currency(global_total_amount, grouping=True).replace('?','₹')
		tree_ar.append(['Global: ' + amount_dict['Global'], None, float(global_total_amount), int(global_total_amount)])
		
		# Adding project categories
		projectcategories = self.dbsession.query(ProjectCategory).all()
		for projectcategory in projectcategories:
			category_total_amount = self.dbsession.query(func.sum(Project.amount_total)) \
												.filter(Project.category_id==projectcategory.id) \
												.scalar()
			amount_dict[str(projectcategory.name)] = locale.currency(category_total_amount, grouping=True).replace('?','₹')
			tree_ar.append(
				[
					str(projectcategory.name) + ': ' + amount_dict[str(projectcategory.name)],
					'Global: ' + amount_dict['Global'], 
					float(category_total_amount), 
					int(category_total_amount)
				]
			)
		
		cat_names = [cat.name for cat in projectcategories]

		# Adding project sub categories
		projectsubcategories = self.dbsession.query(ProjectSubCategory).all()
		for projectsubcategory in projectsubcategories:
			sub_category_total_amount = self.dbsession.query(func.sum(Project.amount_total)) \
												.filter(Project.subcategory_id==projectsubcategory.id) \
												.scalar()
			if projectsubcategory.name in cat_names:
				projectsubcategory.name = projectsubcategory.name + ' '
			tree_ar.append(
				[
					str(projectsubcategory.name) + ': ' + locale.currency(sub_category_total_amount, grouping=True).replace('?','₹'),
					str(projectsubcategory.category.name) + ': ' + amount_dict[projectsubcategory.category.name], 
					float(sub_category_total_amount), 
					int(sub_category_total_amount)
				]
			)

		subcat_names = [subcat.name for subcat in projectsubcategories]

		# # Adding projects
		# projects = self.dbsession.query(Project).all()
		# proj_names = [proj.name for proj in projects]
		# for project in projects:
		# 	if project.name in subcat_names \
		# 	or project.name in cat_names \
		# 	or proj_names.count(project.name) > 1:
		# 		project.name = project.name + '-' + str(project.id)
		# 	tree_ar.append([str(project.name), str(project.subcategory.name), float(project.amount_total), project.city.id])

		return tree_ar

	def get_phases_treemap_json(self):

		locale.setlocale(locale.LC_MONETARY, 'enn')

		# Header for google data
		tree_ar = [['Title', 'Parent', 'Amount', 'City']]
		
		amount_dict = {}

		# Total amount of all the projects
		global_total_amount = self.dbsession.query(func.sum(Project.amount_total)).scalar()
		amount_dict['Global'] = locale.currency(global_total_amount, grouping=True).replace('?','₹')
		tree_ar.append(['Global: ' + amount_dict['Global'], None, float(global_total_amount), int(global_total_amount)])
		phases = []
		cat_names = []
		subcat_names = []
		# Add phases/rounds
		for value in self.dbsession.query(Project.round).distinct():
			if value:
				phase_name = value[0]
				phases.append(phase_name)
				phase_amount = self.dbsession.query(func.sum(Project.amount_total)) \
												.filter(Project.round==phase_name) \
												.scalar()
				amount_dict[phase_name] = locale.currency(phase_amount, grouping=True).replace('?','₹')
				tree_ar.append(
					[
						'Phase ' + phase_name + ': ' + amount_dict[phase_name],
						'Global: ' + amount_dict['Global'],
						float(phase_amount),
						int(phase_amount)
					]
				)

		projects = self.dbsession.query(Project).all()
		
		# Adding project categories by phase
		for phase in phases:
			phase_projects = [project for project in projects if project.round == phase]
			for phase_project in phase_projects:
				category = phase_project.category
				phase_cat_name = 'Phase ' + phase + ' ' + category.name
				if phase_cat_name not in cat_names:
					cat_names.append(phase_cat_name)
					phase_category_projects = [category_phase_project for category_phase_project in phase_projects if category_phase_project.category.id == category.id]

					phase_category_total_amount = sum(phase_category_project.amount_total for phase_category_project in phase_category_projects)

					amount_dict[phase_cat_name] = locale.currency(phase_category_total_amount, grouping=True).replace('?','₹')
					tree_ar.append(
						[
							phase_cat_name + ': ' + amount_dict[phase_cat_name], 
							'Phase ' + phase + ': ' + amount_dict[phase],
							float(phase_category_total_amount), 
							int(phase_category_total_amount)
						]
					)
				subcategory = phase_project.subcategory
				phase_subcat_name = 'Phase ' + phase + ' ' + subcategory.name
				if phase_subcat_name not in subcat_names:
					subcat_names.append(phase_subcat_name)
					phase_subcat_projects = [phase_subcat_project for phase_subcat_project in phase_projects if phase_subcat_project.subcategory.id == subcategory.id]
					phase_subcat_total_amount = sum(phase_subcat_project.amount_total for phase_subcat_project in phase_subcat_projects)
					amount_dict[phase_subcat_name] = locale.currency(phase_subcat_total_amount, grouping=True).replace('?','₹')
					tree_ar.append([
							phase_subcat_name + ': ' + amount_dict[phase_subcat_name],
							phase_cat_name + ': ' + amount_dict[phase_cat_name],
							float(phase_subcat_total_amount),
							int(phase_subcat_total_amount)
						]
					)

		# # Adding projects
		# for project in projects:
		# 	project_total_amount = project.amount_total
		# 	tree_ar.append(
		# 		[
		# 			str(project.name) + ': ' + locale.currency(project_total_amount, grouping=True).replace('?','₹'), 
		# 			'Phase ' + str(project.round) + ': ' + amount_dict[project.round],
		# 			float(project_total_amount),
		# 			int(project_total_amount)
		# 		]
		# 	)

		return tree_ar

	def get_states_treemap_json(self):

		locale.setlocale(locale.LC_MONETARY, 'enn')

		# Header for google data
		tree_ar = [['Title', 'Parent', 'Amount', 'City']]
		
		amount_dict = {}

		# Total amount of all the projects
		global_total_amount = self.dbsession.query(func.sum(Project.amount_total)).scalar()
		amount_dict['Global'] = locale.currency(global_total_amount, grouping=True).replace('?','₹')
		tree_ar.append(['Global: ' + amount_dict['Global'], None, float(global_total_amount), int(global_total_amount)])
		states = []
		cat_names = []
		subcat_names = []
		
		# Add states
		for state in self.dbsession.query(State).all():
			cities = self.dbsession.query(City.id).filter(City.state_id==state.id).all()
			state_amount = self.dbsession.query(func.sum(Project.amount_total)) \
											.filter(Project.city_id.in_(cities)) \
											.scalar()
			amount_dict[state.name] = locale.currency(state_amount, grouping=True).replace('?','₹')
			tree_ar.append(
				[
					state.name + ': ' + amount_dict[state.name],
					'Global: ' + amount_dict['Global'],
					float(state_amount),
					int(state_amount)
				]
			)

			# Adding project categories by state
			state_projects = self.dbsession.query(Project).filter(Project.city_id.in_(cities)).all()
			for state_project in state_projects:
				category = state_project.category
				state_cat_name = state.name + ' ' + category.name
				if state_cat_name not in cat_names:
					cat_names.append(state_cat_name)
					state_category_projects = [category_state_project for category_state_project in state_projects if category_state_project.category.id == category.id]

					state_category_total_amount = sum(state_category_project.amount_total for state_category_project in state_category_projects)

					amount_dict[state_cat_name] = locale.currency(state_category_total_amount, grouping=True).replace('?','₹')
					tree_ar.append(
						[
							state_cat_name + ': ' + amount_dict[state_cat_name], 
							state.name + ': ' + amount_dict[state.name],
							float(state_category_total_amount), 
							int(state_category_total_amount)
						]
					)
				subcategory = state_project.subcategory
				state_subcat_name = state.name + ' ' + subcategory.name
				if state_subcat_name not in subcat_names:
					subcat_names.append(state_subcat_name)
					state_subcat_projects = [state_subcat_project for state_subcat_project in state_projects if state_subcat_project.subcategory.id == subcategory.id]
					state_subcat_total_amount = sum(state_subcat_project.amount_total for state_subcat_project in state_subcat_projects)
					amount_dict[state_subcat_name] = locale.currency(state_subcat_total_amount, grouping=True).replace('?','₹')
					tree_ar.append([
							state_subcat_name + ': ' + amount_dict[state_subcat_name],
							state_cat_name + ': ' + amount_dict[state_cat_name],
							float(state_subcat_total_amount),
							int(state_subcat_total_amount)
						]
					)

		return tree_ar

	def get_cities_treemap_json(self):

		locale.setlocale(locale.LC_MONETARY, 'enn')

		# Header for google data
		tree_ar = [['Title', 'Parent', 'Amount', 'City']]
		
		amount_dict = {}

		# Total amount of all the projects
		global_total_amount = self.dbsession.query(func.sum(Project.amount_total)).scalar()
		amount_dict['Global'] = locale.currency(global_total_amount, grouping=True).replace('?','₹')
		tree_ar.append(['Global: ' + amount_dict['Global'], None, float(global_total_amount), int(global_total_amount)])
		cities = []
		cat_names = []
		subcat_names = []
		
		# Add states
		for city in self.dbsession.query(City).all():
			cities.append(city)
			city_amount = self.dbsession.query(func.sum(Project.amount_total)) \
											.filter(Project.city_id==city.id) \
											.scalar()
			amount_dict[city.name] = locale.currency(city_amount, grouping=True).replace('?','₹')
			tree_ar.append(
				[
					city.name + ': ' + amount_dict[city.name],
					'Global: ' + amount_dict['Global'],
					float(city_amount),
					int(city_amount)
				]
			)

			# Adding project categories by city
			city_projects = self.dbsession.query(Project).filter(Project.city_id==city.id).all()
			for city_project in city_projects:
				category = city_project.category
				city_cat_name = city.name + ' ' + category.name
				if city_cat_name not in cat_names:
					cat_names.append(city_cat_name)
					city_category_projects = [category_state_project for category_state_project in city_projects if category_state_project.category.id == category.id]

					city_category_total_amount = sum(city_category_project.amount_total for city_category_project in city_category_projects)

					amount_dict[city_cat_name] = locale.currency(city_category_total_amount, grouping=True).replace('?','₹')
					tree_ar.append(
						[
							city_cat_name + ': ' + amount_dict[city_cat_name], 
							city.name + ': ' + amount_dict[city.name],
							float(city_category_total_amount), 
							int(city_category_total_amount)
						]
					)
				subcategory = city_project.subcategory
				city_subcat_name = city.name + ' ' + subcategory.name
				if city_subcat_name not in subcat_names:
					subcat_names.append(city_subcat_name)
					city_subcat_projects = [city_subcat_project for city_subcat_project in city_projects if city_subcat_project.subcategory.id == subcategory.id]
					city_subcat_total_amount = sum(city_subcat_project.amount_total for city_subcat_project in city_subcat_projects)
					amount_dict[city_subcat_name] = locale.currency(city_subcat_total_amount, grouping=True).replace('?','₹')
					tree_ar.append([
							city_subcat_name + ': ' + amount_dict[city_subcat_name],
							city_cat_name + ': ' + amount_dict[city_cat_name],
							float(city_subcat_total_amount),
							int(city_subcat_total_amount)
						]
					)

		return tree_ar