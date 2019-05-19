"""
watch list

https://www.youtube.com/watch?v=s1H8EzGGPLA
https://www.youtube.com/watch?v=MmKY00znzNE&list=PLfNW_1ECVaTh6m39Ecz6opUsyAfTCPyuS&index=3
https://www.youtube.com/results?search_query=color+scheme+for+mens+dress
https://www.youtube.com/watch?v=okaHQL2oVAs
https://www.youtube.com/watch?v=hw_ie8PUXGI
https://www.youtube.com/watch?v=-vRKFWxJaU4


Need to implement:
Black and white [white != white] applicable for pant only
but test for both bottoms and tops can not white == white, at least one have to be different
"""


"""
Video info
Focus Basic Style, Then follow trend for experiment
vneck T-shirt -Navy blue,gray,dark brown,dark green,black, white
Shoe,Shades, watch - quality
Tshirt - quantity
Foucs on versatile dress which never goes out of fashion

Formal, Middle, Causual
Pricy materlial like Leather, swell, canvas/sneaker/fabric

Lofar is versatile dress and ocation
'Tassel Lofar','Horsebit Lofar','Penny Lofar',''
'Tassel Lofar' : "on front 2 laise spreaded, shiny, formal"
'Horsebit Lofar' : "A strap attaching two square ring, swell material"
'Penny Lofar' : "formal and adult"


T shirt
Young - Pattern, bright or color
Average - Dark tshirt with pattern, plain t-shirt bright in color
Mature - plain, dark or white in color
Graphics - 2 color maximum, 3rd color will cover minimal if present
No logo - logo shows budget, plain simple is good
fit - when raise your arm, tshirt should not expose any skin. ends in the middle of groin section. short and tight sleves, not so tight it shows you are desperate. tight in upper torso, loose in mid torso. everything above nipple should be tigher and below more loose.
neck ring - keep it tight, closer to body, neck ring thin.

Buy few classic peaces, 
Primary: Black V-neck T-shirt,White V-neck T-shirt, White roundneck-neck T-shirt,
Secondary: Navy Blue, Brown , Olive green, Solid grey
Tarsiary: Maroon, Deep Blue

Causual
T-shirt != Formal Shoes
T-shirt != Boot,Lofer
T-shirt == Sneaker,Flip-Flop
T-shirt != No Metalic watches
T-shirt == Leather Strap watches
Shirt == Metalic watches
Semi formal - Plan white/black Tshirt with formal jacket

Office,Date
Polo Tshirt, Shirt

sum----
Tshirt: plain, dark/light, no logo,
tight & thin neck ring


Color matching video
[Deep Blue Denim Jeans - Mathing with any tops
Black and white [white != white] tshirt
tshirt navyblue and grey [specially for this 2 color and also applicable for others color: satured with unsatured >> pant and top]
earthy color: brown and olive green, with black, stylish
bright color: sexy ['light yellow':'#fce599', 'light orange':'#DA9B6F', 'light pink':'#F9E6F9', 'white blue':'#DCF0FA', 'sky blue':'#87CEFA']
#pants can not be white and of light sexy color or tarsiary color

pants
black , not white
navyblue grey
tarsiary colors]


Video info

How to determine skin tone, warm, cool or neutral
https://www.youtube.com/watch?v=hw_ie8PUXGI
"""


"""
No to wear Books
"""
#pants can not be white #not applicable or sure for others bottoms short,lungi,dhuti
#pants can not be of bright color #not applicable or sure for others bottoms short,lungi,dhuti
#tshirt is informal, so can't be wear with semi formal or formal shoes
#T-shirt != No Metalic watches[Formal] , semi-formal and causual is ok
"""
No to wear Books
"""


def select_type():
	pass
def select_color():
	pass

color = {
'primary':{
	'black':'#252024','white':'#F5F5F5'
	},
'secondary':{
	'navyblue':'#233963','grey':'#8a9096'
	},
'earthy':{
	'brown':'#774e3b','olivegreen':'#6b8254'
	},
'bright & light':{
	'light yellow':'#fce599', 'light orange':'#DA9B6F', 'light pink':'#F9E6F9', 'white blue':'#DCF0FA', 'sky blue':'#87CEFA'
	}
}
#maroon - bright color missing as it doesn't go for all

saturation = ['saturated','unsatured']


#Sections
bottoms = {'pants':{},'jeans':{}}
tops = {'shirts':{},'tshirt':{'roundneck':'','vneck':''},'polots_hirt':{}}
#{'1':'','2':''}
shoes = ['boot','lofar','sneaker','flipflop']
belts = {}

#formal, semi-formal, formal watch
watches = {'metalic watch':{'rounded':''},'leather strap watch':{'rounded':''},'digital watch':''} #optional
shades = {'round','square','innerv'} #optional

def check_if_optional(li):
	if None in li:
		print("Optional item")
def combinations(lia,lib):
	return [(x,y) for x in lia for y in lib]
	
	

def return_types(elemnts):
	result_li = []
	if elemnts == None:
		pass
	if not type(elemnts) == list:
		for key in elemnts:
			item = elemnts[key]
			#print(str(item) + str(type(item)))
			if(item == {} or item == ''):
				#print("last value")
				result_li.append(key)
			elif(type(item) == dict):
				#if(type(item[key]) == str):
				#	this is a value
				# ignore last value, take key
				result_li = result_li + [key + ' ' + i  for i in return_types(item)]
			elif(type(item) == list):
				result_li = result_li + [key + ' ' + a for a in item]
			elif(type(item) == str):
				pass
	else:
		result_li = elemnts

	return result_li

def return_colors(color_type):
	return color[color_type]

def buy_flow():
	print("Select type")
	print("Select color")
	print("Select fit")
	print("Select price range")

def li_in_str(lis,str):
	for li in lis:
		if li in str:
			return True


def select_single_item(elemnts,color_type):
	def cancelling_rules(item,debug=False):
		first,second = item
		#cancelling rule
		if(li_in_str(bottoms,first) or li_in_str(bottoms,second)):
			#pants can not be white #not applicable or sure for others bottoms short,lungi,dhuti
			if('white' in item):
				if(debug): print("cancelled "+str(item)+" >> white color bottoms")
				return False
			#pants can not be of bright color #not applicable or sure for others bottoms short,lungi,dhuti
			elif(li_in_str(color['bright & light'],first) or li_in_str(color['bright & light'],second)):
				if(debug): print("cancelled "+str(item)+" >> bright & light color bottoms")
				return False
		return item
	
	alls = combinations(return_types(elemnts),return_colors(color_type))
	result_set = [item for item in alls if(cancelling_rules(item,debug=False))]
	return result_set
	

def get_item_combination(item_section_1,item_section_2):
	def cancelling_rules_com(item,debug=False):
		item_1,item_2 = item
		if(li_in_str(tops,item_1) or li_in_str(tops,item_2)): #if top
			if('tshirt' in item_1 or 'tshirt' in item_2): #if tshirt
				#tshirt is informal, so can't be wear with semi formal or formal shoes
				if li_in_str(['boot','lofar'],item_1) or li_in_str(['boot','lofar'],item_2):
					if(debug): print("cancelled "+str(item)+" >> tshirt is informal, so can't be wear with semi formal or formal shoes")
					return False
				#T-shirt != No Metalic watches[Formal] , semi-formal and causual is ok
				if('metalic watch' in item_1 or 'metalic watch' in item_2):
					if(debug): print("cancelled "+str(item)+" >> tshirt is informal, so can't be wear with semi formal or formal watches")
					return False
		return item

	all_combinations = combinations(item_section_1,item_section_2)
	filtered_set = [item for item in all_combinations if(cancelling_rules_com(item,debug=False))]
	combine_look = [item_1 + item_2 for item_1,item_2 in filtered_set]
	return combine_look

def get_yours_combinations():
	#add color passing system
	bottoms = {'pants':{},'jeans':{}}
	tops = {'shirts':{}}
	#{'1':'','2':''}
	shoes = ['sneaker','flipflop']
	belts = {}
	watches = {'leather strap watch':{'rounded':''}}
	glasses = {}

	item_section_1 = select_single_item(tops,'primary')
	item_section_2 = select_single_item(shoes,'primary')
	item_section_3 = select_single_item(watches,'primary')
	
	item_section_1 = [type_ + " " + color + "," for type_,color in item_section_1]
	item_section_2 = [type_ + " " + color + "," for type_,color in item_section_2]
	item_section_3 = [type_ + " " + color + "," for type_,color in item_section_3]

	combinations_1 = get_item_combination(item_section_1,item_section_2)
	combinations_2 = get_item_combination(combinations_1,item_section_3)
	for look in combinations_2:
		print(look)
	print("Your possible Looks = "+str(len(combinations_2)))


def main():
	item_section_1 = select_single_item(tops,'primary')
	item_section_2 = select_single_item(shoes,'primary')
	item_section_3 = select_single_item(watches,'primary')
	
	item_section_1 = [type_ + " " + color + "," for type_,color in item_section_1]
	item_section_2 = [type_ + " " + color + "," for type_,color in item_section_2]
	item_section_3 = [type_ + " " + color + "," for type_,color in item_section_3]

	combinations_1 = get_item_combination(item_section_1,item_section_2)
	combinations_2 = get_item_combination(combinations_1,item_section_3)
	for look in combinations_2:
		print(look)
	print(len(combinations_2))
	

if __name__ == "__main__":
	#get_yours_combinations()
	main()


