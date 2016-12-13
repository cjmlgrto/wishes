from flask import Flask, render_template, redirect, request
from models import *

groups = {
	'Family A': ['Jack', 'John', 'Jill', 'Jefferson', 'Joanna'],
	'Family B': ['Carol', 'Charles', 'Cosette', 'Castle'],
	'Family C': ['Robert', 'Rhianna', 'Randy', 'Riley', 'Reyna'],
	'Family D': ['Elizabeth', 'Ezra', 'Elaine', 'Eric', 'Ester', 'Emanuel'],
	'Family E': ['Tina', 'Tim', 'Terry', 'Tatiana', 'Toby']
}

app = Flask(__name__)

# Database connect
# ------------------------
@app.before_request
def before_request():
	init()

# Database disconnect
# ------------------------
@app.teardown_request
def teardown_request(exception):
	db.close()

# Display groups
# ------------------------
@app.route('/')
def display_groups():
	return render_template('groups.html', groups=groups)

# Display group
# ------------------------
@app.route('/<group_id>')
def display_group(group_id=None):
	if group_id is None:
		return redirect('/')
	else:
		group = group_id.replace('-',' ').title()
		if group in groups:
			members = groups[group]
			return render_template('group.html', members=members, group=group_id)
		else:
			return redirect('/')

# Display member
# ------------------------
@app.route('/<group_id>/<member_id>')
def display_member(group_id=None, member_id=None):
	if group_id is None or member_id is None:
		return redirect('/')
	else:
		group = group_id.replace('-',' ').title()
		member = member_id.title()
		if group in groups and member in groups[group]:
			db_member = Member.select().where(Member.name==member)[0]
			wishlist_str = db_member.wishlist
			if wishlist_str == '':
				wishlist = False
			else:
				wishlist = wishlist_str.split('###')
			metrics = db_member.metrics.split('###')

			return render_template('member.html', group=group_id, member=member, wishlist=wishlist, metrics=metrics)
		else:
			return redirect('/')

# Display edit mode
# ------------------------
@app.route('/edit/<group_id>/<member_id>')
def display_member_edit(group_id=None, member_id=None):
	if group_id is None or member_id is None:
		return redirect('/')
	else:
		group = group_id.replace('-',' ').title()
		member = member_id.title()
		if group in groups and member in groups[group]:
			db_member = Member.select().where(Member.name==member)[0]
			wishlist_str = db_member.wishlist
			if wishlist_str == '':
				wishlist = False
			else:
				wishlist = wishlist_str.split('###')
			metrics = db_member.metrics.split('###')
			return render_template('member-edit.html', group=group_id, member=member, wishlist=wishlist, metrics=metrics)
		else:
			return redirect('/')

# Add item
# ------------------------
@app.route('/add/<group_id>/<member_id>', methods=['POST'])
def add(group_id, member_id):
	item_id = request.form['new_item']

	if item_id == '' or item_id is None:
		return redirect('/edit/' + group_id + '/' + member_id)

	member = member_id.title()

	db_member = Member.select().where(Member.name==member)[0]

	wishlist_str = db_member.wishlist
	if wishlist_str[:3] == '###':
		db_member.wishlist = wishlist_str[3:] + '###' + item_id
	elif wishlist_str == '':
		db_member.wishlist = item_id
	else:
		db_member.wishlist += '###' + item_id
	db_member.save()

	return redirect('/edit/' + group_id + '/' + member_id)

# Delete item
# ------------------------
@app.route('/delete/<group_id>/<member_id>/<item_id>')
def delete(group_id, member_id, item_id):
	member = member_id.title()
	item = item_id.replace('zzz','/').replace('%20', ' ')

	db_member = Member.select().where(Member.name==member)[0]

	wishlist_array = db_member.wishlist.split('###')
	wishlist_array.remove(item)
	wishlist_array = [x for x in wishlist_array if x != '']
	wishlist_str = '###'.join(wishlist_array)
	
	db_member.wishlist = wishlist_str
	db_member.save()

	return redirect('/edit/' + group_id + '/' + member_id)

# Toggle checked/unchecked
# ------------------------
@app.route('/toggle/<group_id>/<member_id>/<item_id>')
def toggle(group_id, member_id, item_id):
	member = member_id.title()
	item = item_id.replace('zzz','/')

	db_member = Member.select().where(Member.name==member)[0]

	wishlist_array = db_member.wishlist.split('###')
	i = wishlist_array.index(item)
	if wishlist_array[i][:6] == '@done:':
		wishlist_array[i] = wishlist_array[i][6:]
	else:
		wishlist_array[i] = '@done:' + wishlist_array[i]
	wishlist_str = '###'.join(wishlist_array)

	db_member.wishlist = wishlist_str
	db_member.save()

	return redirect('/' + group_id + '/' + member_id)

# Save metrics
# ------------------------
@app.route('/save/<group_id>/<member_id>', methods=['POST'])
def save(group_id, member_id):
	shirt = request.form['shirt']
	pants = request.form['pants']
	shoes = request.form['shoes']

	if shirt.strip() == '':
		shirt = '?'

	if pants.strip() == '':
		shirt = '?'

	if shoes.strip() == '':
		shirt = '?'

	member = member_id.title()
	db_member = Member.select().where(Member.name==member)[0]

	if shirt.strip() != '' and pants.strip() != '' and shoes.strip() != '':
		metrics_array = db_member.metrics.split('###')
		metrics_array[0] = shirt
		metrics_array[1] = pants
		metrics_array[2] = shoes
		metrics_str = '###'.join(metrics_array)
		db_member.metrics = metrics_str
		db_member.save()

	return redirect('/' + group_id + '/' + member_id)

# Search
# ------------------------
@app.route('/search', methods=['POST'])
def search():
	query = request.form['query'].lower()
	members = []
	for group in groups:
		for member in groups[group]:
			if member.lower().startswith(query):
				members.append((member, group))
	if len(members) < 1:
		found = False
	else:
		found = True

	return render_template('search.html', members=members, found=found, query=query)

# Reset
# ------------------------
@app.route('/reset')
def reset():
	for group in groups:
		for member in groups[group]:
			temp = Member.create(name=member, wishlist='Apple###Banana###Carrot', metrics='?###?###?')
	return 'Database reset!'


# Run the app
# ------------------------
if __name__ == '__main__':
	app.run()