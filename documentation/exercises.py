## muscle anatomy videos - https://www.youtube.com/watch?v=Kkqjfc7EYvM
# Order due to back pain,
# Leg, Hands, Abs,
Muscles = ['Deltoids','Triceps','Biceps','Forearm','Trapezius','Middle Back','Latissimus Dorsi','Lower Back','Quadriceps','Calves','Hamstring','Upper Abs','Lower Abs','Obliques']

Muscle_Groups = {
	'Hand':{
		'Deltoids':{'general_name':'Shoulders','parts':'Front,Middle,Rear'},
		'Triceps':{'general_name':'','parts':'Front,Middle,Rear'},
		'Biceps':{'general_name':'','parts':'Inner,Outter'},
		'Forearm':{'general_name':'','parts':''}
	},
	'Chest':{'general_name':'','parts':'Upper,Middle,Lower'},
	'Back':{
		'Trapezius':{'general_name':'Trap','parts':''},
		'Middle Back':{'general_name':'','parts':''},
		'Latissimus Dorsi':{'general_name':'Lat','parts':''},
		'Lower Back':{'general_name':'','parts':''}
	},
	'Leg':{
		'Quadriceps':{'general_name':'','parts':'','comment':'4 muscles'},
		'Calves':{'general_name':'','parts':'Gastronemius,Soleus'},
		'Hamstring':{'general_name':'','parts':''}
	},
	'Abs':{'general_name':'','parts':'Upper,Lower,Obliques'}
}
Shoulders = {
	'Dumbell Front Raises':[
		{'target':'Front Head of Deltoids'},
		{'type':'isolation'},
		{'instrument':'Dumbell'},
		{'comment':'Start with this exercise if you are weaker in this muscle group.'}
	],
	'Dumbell Side Raises':[
		{'target':'Side Head of Deltoids or Outer Deltoids'},
		{'type':'isolation'},
		{'instrument':'Dumbell'},
		{'comment':'Puts caps on your shoulders & gives the illusion of a smaller waist.'}
	],
	'Dumbell Rear Delt Raises':[
		{'target':'Rear Head of Deltoids or Rear Deltoids'},
		{'type':'isolation'},
		{'instrument':'Dumbell'},
		{'comment':'Harder to isolate. So keep strict form and go a little lighter to build mind and muscle connection.'}
	],
	'Shoulder Press':[
		{'target':'front and outer or side head of Deltoid muscle'}
		{'type':'compound'},
		{'instrument':'Dumbell or Barbell weight'},
		{'comment':''}
	]
}

Triceps = {
	'Cable Tricep Pushdowns':[
		{'target':'Outer head of Tricep'},
		{'type':'isolation'},
		{'instrument':'cable pullie weight'},
		{'comment':''}
	],
	'Skull Crushers':[
		{'target':'Middle head of Tricep'},
		{'type':'isolation'},
		{'instrument':'Barbell weight'},
		{'comment':''}
	],
	'Overhead Dumbell Extension':[
		{'target':'Rear head of Tricep'},
		{'type':'isolation'},
		{'instrument':'Dumbell'},
		{'comment':''}
	],
	'Overhead Cable Extension':[
		{'target':''},
		{'type':''},
		{'instrument':''},
		{'comment':''}
	],
	'Close Grip Bench Presses':[
		{'target':''},
		{'type':''},
		{'instrument':''},
		{'comment':''},
		{'resources':'https://www.youtube.com/watch?v=Nv43VSWWGtc','https://www.youtube.com/watch?v=QVmE6bbBtwo'}
	],
}

#Supernated(Bicep Curl), Pronated(Opposite position of Bicep Curl), Neutral position forearm
Biceps = {
	'Wide Grip Bicep Curls':[
		{'target':'Inner Head of Bicep'},
		{'type':'isolation'},
		{'instrument':'Barbell weight or tricky posture dumble weight'},
		{'comment':''}
	],
	'Hammer Curls':[
		{'target':'Outer Head of Bicep'}
		{'type':'isolation'},
		{'instrument':'Dumbell'},
		{'comment':''}
	],
	'Preacher Curls':[
		{'target':'Overall 2 head of Biceps'},
		{'type':'isolation'},
		{'instrument':''},
		{'comment':'There are several options for neutral grip biceps.'}
	],

	
}

Back = {
	'Shrugs':[
		{'target':'Top head of Trapezius'},
		{'type':'isolation'},
		{'instrument':'Dumbell'},
		{'comment':''}
	],
	'Lat Pulldown':[
		{'target':'Lats'},
		{'type':'isolation'},
		{'instrument':'Lat Pulldown Machine'},
		{'comment':'For thickness and V taper'}
	],
	'Behind the Neck Lat Pulldown':[
		{'target':''},
		{'type':'isolation'},
		{'instrument':'Lat Pulldown Machine'},
		{'comment':''}
	],
	'Close Grip Lat Pulldown':[
		{'target':''},
		{'type':'isolation'},
		{'instrument':'Lat Pulldown Machine'},
		{'comment':''}
	],
	'Pullups':[
		{'target':''},
		{'type':''},
		{'instrument':'Lat Pulldown Machine'},
		{'comment':''}
	],
	'Seated Cable Row':[
		{'target':'Overall Back'},
		{'type':'compound'},
		{'instrument':'Cable pollie weight'},
		{'comment':'For overall thickness and width'}
	],
	'Bent Over Rows':[
		{'target':''},
		{'type':''},
		{'instrument':''},
		{'comment':''}
	],
	'Cable Polley Rows':[
		{'target':''},
		{'type':''},
		{'instrument':''},
		{'comment':''}
	],
	'Single Dumbell Rows':[
		{'target':''},
		{'type':''},
		{'instrument':''},
		{'comment':''}
	],	
	'Dumbell Deadlifts':[
		{'target':'Lower Back'},
		{'type':'isolation'},
		{'instrument':'Dumbell'},
		{'comment':''}
	],
	'Hyper Extension':[
		{'target':'Lower Back'},
		{'type':'isolation'},
		{'instrument':'Hyper Extension Machine'},
		{'comment':''}
	]
	
}

Chest = {
	'Incline Dumbell Flyes':[
		{'target':'Upper Chest'},
		{'type':'isolation'},
		{'instrument':'Dumbell and Incline Bench'},
		{'comment':''}
	],
	'Incline Dumbell Flyes':[
		{'target':'Upper Chest'},
		{'type':'isolation'},
		{'instrument':'Dumbell and Incline Bench'},
		{'comment':''}
	],
	'Flat Chest Dumbell Press':[
		{'target':'Middle Chest'},
		{'type':'isolation'},
		{'instrument':'Dumbell and Flat Bench'},
		{'comment':'Arm should come down at the Middle of the Chest'}
	],
	'Cable Crossover':[
		{'target':'Lower Chest'},
		{'type':'isolation'},
		{'instrument':'Cable duel chest polleies'},
		{'comment':''}
	],
	'Decline Bench Press':[
		{'target':'Lower Chest'},
		{'type':'isolation'},
		{'instrument':'Barbell weight and Decline Bench'},
		{'comment':''}
	],
}

Abs = {
	'Weighted Crunches':[
		{'target':'Upper Abs'},
		{'type':'isolation'},
		{'instrument':'weight'},
		{'comment':'Added weight allows you go to failure in lower reps.'}	
	],
	'Roman Situps':[
		{'target':'Upper Abs'},
		{'type':'isolation'},
		{'instrument':'Decline Abs bench'},
		{'comment':''}	
	],
	'Lying Leg Raises':[
		{'target':'Lower Abs'},
		{'type':'isolation'},
		{'instrument':''},
		{'comment':''}	
	],
	'Hanging Leg Raises':[
		{'target':'Lower Abs'},
		{'type':'isolation'},
		{'instrument':'Hanging place'},
		{'comment':''}	
	]
}
Leg = {
	'Leg Extension':[
		{'target':'Quadriceps'}
		{'type':'isolation'},
		{'instrument':'Hanging place'},
		{'comment':'Target all 4 Quadriceps muscle. Great to start with, It warm up your knees. It prefatigue your quads before moving into compound exercise.'}
	],
	'Sqauts':[
		{'target':'Quads AND Hamstring'}
		{'type':'compound'},
		{'instrument':'Barbell weight'},
		{'comment':''}
	],
	'Leg press':[
		{'target':'Quads AND Hamstring'}
		{'type':'compound'},
		{'instrument':'Leg Press Machine'},
		{'comment':'Further you keep your feet up on leg press platform from neutral feet position, it will hit more Hamstring. In neutral position it will hit more your quads muscle.'}		
	],
	'Dumbell Lunges':[
		{'target': 'Quads,Hamstring,Glutes'},
		{'type':'compound'},
		{'instrument':'Dumbell'}
	],
	'Barbell Lunges':[
		{'target': 'Quads,Hamstring,Glutes'},
		{'type':'compound'},
		{'instrument':'Barbell'}
	],
	'Hamstring Curls':[
		{'target': 'Hamstring'},
		{'type':'isolation'},
		{'instrument':'Barbell'}
		{'comment':'Great to warm up your joints before performing a compound workout.'}
	],
	'Seated Calf Press':[
		{'target': 'Lower Calves(Soleus)'},
		{'type': 'isolation'},
		{'instrument':''}
		{'comment':'It works the lower part of calf.'}
	],
	'Standing Calf Press':[
		{'target': 'Calves'},
		{'type': 'isolation'},
		{'instrument':'Hack Squat Machine'},
		{'comment':'This works the belly of the calf.'}
	]
}
## Obliques don't train them ,  as they are worked during other exercises, Can give you a square or boxy look.
## Weighted obleque crunch, cable pull obleques