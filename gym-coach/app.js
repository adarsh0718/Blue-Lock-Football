/* =========================================================
   EXERCISE DATABASE
   Each muscle group has entries per equipment tier.
   ========================================================= */
const EX = {
  chest: {
    gym: [
      {name:"Barbell Bench Press", sets:4, reps:"6–8", rest:"2–3 min", tempo:"3-0-1-1",
       form:"Retract shoulder blades, feet flat, bar path travels to lower chest, elbows ~45° from torso.",
       mistake:"Flaring elbows to 90° and bouncing the bar off the chest.",
       tip:"Drive feet into the floor and keep upper back tight throughout the set.",
       beginnerAlt:"Machine chest press for controlled bar path.",
       advancedVar:"Pause bench press (2-sec pause on chest) or add chains/bands."},
      {name:"Incline Dumbbell Press", sets:3, reps:"8–12", rest:"90 sec", tempo:"2-0-1-1",
       form:"Bench at 30–45°, press dumbbells up and slightly inward, full stretch at bottom.",
       mistake:"Setting the incline too steep, which shifts load to front delts.",
       tip:"Squeeze chest at the top instead of locking elbows hard.",
       beginnerAlt:"Incline machine press.",
       advancedVar:"1.5-rep incline press for extended time under tension."}
    ],
    home: [
      {name:"Dumbbell Bench/Floor Press", sets:4, reps:"8–12", rest:"90 sec", tempo:"2-0-1-1",
       form:"On floor or bench, press dumbbells straight up, elbows finish under wrists.",
       mistake:"Letting shoulders roll forward at lockout.",
       tip:"Pause briefly at the top to reinforce control.",
       beginnerAlt:"Reduce range on floor press (natural floor stop protects shoulders).",
       advancedVar:"Alternate single-arm press for added core demand."},
      {name:"Push-Up Variations", sets:3, reps:"12–20", rest:"60 sec", tempo:"2-0-1-1",
       form:"Straight line from head to heels, hands under shoulders, chest to floor.",
       mistake:"Sagging hips or flaring elbows.",
       tip:"Add a resistance band across your back for extra load.",
       beginnerAlt:"Incline push-ups on a bench or counter.",
       advancedVar:"Deficit push-ups with hands elevated on blocks."}
    ],
    bodyweight: [
      {name:"Standard Push-Up", sets:4, reps:"10–20", rest:"60–90 sec", tempo:"2-0-1-1",
       form:"Rigid plank, lower chest to just above floor, full lockout at top.",
       mistake:"Partial range of motion.",
       tip:"Slow the eccentric (lowering) phase to 3 seconds for more growth stimulus.",
       beginnerAlt:"Knee push-ups or wall push-ups.",
       advancedVar:"Archer push-ups or one-arm progression."},
      {name:"Dips (chair/bench)", sets:3, reps:"8–15", rest:"90 sec", tempo:"2-0-1-1",
       form:"Lean forward slightly to bias chest, lower until shoulders are level with elbows.",
       mistake:"Going too deep and straining the shoulder joint.",
       tip:"Keep elbows tracking back, not flared wide.",
       beginnerAlt:"Bent-knee bench dips.",
       advancedVar:"Weighted dips with a backpack."}
    ]
  },
  back: {
    gym: [
      {name:"Barbell Bent-Over Row", sets:4, reps:"6–10", rest:"2 min", tempo:"2-0-1-1",
       form:"Hinge at hips ~45°, pull bar to lower ribs, squeeze shoulder blades together.",
       mistake:"Rounding the lower back to generate momentum.",
       tip:"Brace your core hard before each rep, like resisting a punch.",
       beginnerAlt:"Chest-supported machine row.",
       advancedVar:"Pendlay row (dead-stop each rep)."},
      {name:"Lat Pulldown / Pull-Up", sets:4, reps:"8–12", rest:"90 sec", tempo:"2-0-1-1",
       form:"Pull elbows down and back, lead with chest, avoid using body momentum.",
       mistake:"Yanking with arms only, no scapular retraction.",
       tip:"Think 'elbows to back pockets'.",
       beginnerAlt:"Assisted pull-up machine or band-assisted pull-ups.",
       advancedVar:"Weighted pull-ups."}
    ],
    home: [
      {name:"Single-Arm Dumbbell Row", sets:4, reps:"10–12", rest:"90 sec", tempo:"2-0-1-1",
       form:"Support opposite knee/hand on bench, pull dumbbell to hip, elbow close to body.",
       mistake:"Twisting the torso to complete the rep.",
       tip:"Pause at the top for a 1-second squeeze.",
       beginnerAlt:"Reduce load and focus on range of motion.",
       advancedVar:"Add a slow 4-second eccentric."},
      {name:"Resistance Band Pull-Apart / Row", sets:3, reps:"12–15", rest:"60 sec", tempo:"2-0-1-1",
       form:"Anchor band, pull elbows back keeping arms roughly parallel to floor.",
       mistake:"Using shoulders instead of squeezing shoulder blades.",
       tip:"Slow the return phase to keep tension on the band.",
       beginnerAlt:"Lighter band tension.",
       advancedVar:"Heavier band + pause at full contraction."}
    ],
    bodyweight: [
      {name:"Inverted Row (table/bar)", sets:4, reps:"8–15", rest:"90 sec", tempo:"2-0-1-1",
       form:"Body straight, pull chest to bar, squeeze shoulder blades together.",
       mistake:"Letting hips sag.",
       tip:"Raise feet higher to increase difficulty.",
       beginnerAlt:"Steeper body angle (more upright) to reduce load.",
       advancedVar:"Feet elevated inverted row."},
      {name:"Superman Hold / Reverse Snow Angel", sets:3, reps:"12–15", rest:"60 sec", tempo:"2-1-1-1",
       form:"Lie face down, lift chest and legs slightly, squeeze glutes and upper back.",
       mistake:"Hyperextending the neck.",
       tip:"Keep gaze down to protect the cervical spine.",
       beginnerAlt:"Alternate arm/leg raises instead of full lift.",
       advancedVar:"Add a 2-second hold at peak contraction."}
    ]
  },
  shoulders: {
    gym: [
      {name:"Barbell/DB Overhead Press", sets:4, reps:"6–10", rest:"2 min", tempo:"2-0-1-1",
       form:"Brace core, press straight overhead, avoid excessive lower-back arch.",
       mistake:"Flaring ribs and hyperextending the spine.",
       tip:"Squeeze glutes to keep the torso stacked.",
       beginnerAlt:"Seated machine shoulder press.",
       advancedVar:"Push press using leg drive."},
      {name:"Cable/DB Lateral Raise", sets:3, reps:"12–15", rest:"60 sec", tempo:"2-0-1-1",
       form:"Slight forward lean, raise to shoulder height, lead with elbows.",
       mistake:"Using momentum or shrugging the traps.",
       tip:"Imagine pouring water out of a jug at the top of the movement.",
       beginnerAlt:"Lighter dumbbells, partial range.",
       advancedVar:"Lean-away cable lateral raise for constant tension."}
    ],
    home: [
      {name:"Dumbbell Shoulder Press", sets:4, reps:"8–12", rest:"90 sec", tempo:"2-0-1-1",
       form:"Press dumbbells up and slightly inward, avoid clanging at top.",
       mistake:"Arching the back excessively.",
       tip:"Perform seated on a chair for more stability if needed.",
       beginnerAlt:"Single-arm press with lighter load.",
       advancedVar:"Standing single-arm press for core challenge."},
      {name:"Band Lateral Raise", sets:3, reps:"15–20", rest:"60 sec", tempo:"2-0-1-1",
       form:"Stand on band, raise arms to sides to shoulder height.",
       mistake:"Shrugging shoulders up toward ears.",
       tip:"Keep a slight bend in the elbow throughout.",
       beginnerAlt:"Lighter band.",
       advancedVar:"Slow 4-second lowering phase."}
    ],
    bodyweight: [
      {name:"Pike Push-Up", sets:4, reps:"8–15", rest:"90 sec", tempo:"2-0-1-1",
       form:"Hips high in an inverted-V, lower head toward floor between hands.",
       mistake:"Turning it into a squat by bending knees excessively.",
       tip:"Elevate feet on a step to increase shoulder emphasis.",
       beginnerAlt:"Reduce hip height (less pike angle).",
       advancedVar:"Wall-walk toward handstand push-up."},
      {name:"Arm Circles / Plank Shoulder Taps", sets:3, reps:"20 total", rest:"45 sec", tempo:"controlled",
       form:"In plank, tap opposite shoulder while keeping hips still.",
       mistake:"Rotating hips side to side.",
       tip:"Widen feet stance for more stability.",
       beginnerAlt:"Perform from knees.",
       advancedVar:"Add a push-up between each tap."}
    ]
  },
  legs: {
    gym: [
      {name:"Barbell Back Squat", sets:4, reps:"6–10", rest:"2–3 min", tempo:"3-0-1-1",
       form:"Bar on upper traps, brace core, hips and knees break together, chest up.",
       mistake:"Knees caving inward or heels lifting off the floor.",
       tip:"Push knees out in line with toes throughout the descent.",
       beginnerAlt:"Goblet squat with a dumbbell.",
       advancedVar:"Pause squat (2-sec pause at bottom) or front squat."},
      {name:"Romanian Deadlift", sets:3, reps:"8–12", rest:"2 min", tempo:"3-0-1-1",
       form:"Soft knee bend, hinge at hips, bar/dumbbells stay close to legs.",
       mistake:"Rounding the lower back or turning it into a squat.",
       tip:"Feel a stretch in the hamstrings, stop before back rounds.",
       beginnerAlt:"Dumbbell RDL with lighter load.",
       advancedVar:"Single-leg RDL for added stability demand."}
    ],
    home: [
      {name:"Goblet Squat", sets:4, reps:"10–15", rest:"90 sec", tempo:"2-0-1-1",
       form:"Hold dumbbell at chest, squat between knees, chest stays tall.",
       mistake:"Leaning too far forward.",
       tip:"Elbows can gently brush inside of knees at the bottom.",
       beginnerAlt:"Bodyweight squat first, add load once form is solid.",
       advancedVar:"Bulgarian split squat with rear foot elevated."},
      {name:"Dumbbell Romanian Deadlift", sets:3, reps:"10–12", rest:"90 sec", tempo:"3-0-1-1",
       form:"Hinge hips back, dumbbells slide down thighs, slight knee bend.",
       mistake:"Squatting the weight down instead of hinging.",
       tip:"Keep dumbbells close to the legs the entire rep.",
       beginnerAlt:"Reduce range of motion until hamstring flexibility improves.",
       advancedVar:"Single-leg dumbbell RDL."}
    ],
    bodyweight: [
      {name:"Bodyweight Squat / Jump Squat", sets:4, reps:"15–25", rest:"60–90 sec", tempo:"2-0-1-1",
       form:"Feet shoulder-width, sit hips back and down, knees track over toes.",
       mistake:"Rising onto toes at the top.",
       tip:"Add a 2-second pause at the bottom for more difficulty.",
       beginnerAlt:"Box/chair-assisted squat.",
       advancedVar:"Jump squat for explosive power."},
      {name:"Walking Lunge", sets:3, reps:"12–16 per leg", rest:"90 sec", tempo:"2-0-1-1",
       form:"Step forward, both knees to ~90°, torso upright.",
       mistake:"Front knee traveling far past the toes with poor control.",
       tip:"Push through the front heel to stand.",
       beginnerAlt:"Stationary reverse lunge holding onto a wall.",
       advancedVar:"Add a jump between lunge steps."}
    ]
  },
  glutes: {
    gym: [
      {name:"Barbell Hip Thrust", sets:4, reps:"8–12", rest:"2 min", tempo:"2-1-1-1",
       form:"Upper back on bench, drive hips up, full lockout with ribs down.",
       mistake:"Overextending the lower back at the top.",
       tip:"Pause and squeeze glutes hard for 1 second at the top.",
       beginnerAlt:"Bodyweight glute bridge.",
       advancedVar:"Banded hip thrust for extra top-range tension."}
    ],
    home: [
      {name:"Dumbbell Glute Bridge", sets:4, reps:"12–15", rest:"90 sec", tempo:"2-1-1-1",
       form:"Dumbbell on hips, drive through heels, squeeze glutes at top.",
       mistake:"Pushing through toes instead of heels.",
       tip:"Keep chin tucked to avoid neck strain.",
       beginnerAlt:"Bodyweight bridge only.",
       advancedVar:"Single-leg glute bridge."}
    ],
    bodyweight: [
      {name:"Glute Bridge / Single-Leg Bridge", sets:4, reps:"15–20", rest:"60 sec", tempo:"2-1-1-1",
       form:"Feet hip-width, drive hips up, squeeze at top for a full second.",
       mistake:"Arching the lower back excessively.",
       tip:"Press knees slightly outward to engage glutes over quads.",
       beginnerAlt:"Reduce range of motion.",
       advancedVar:"Single-leg version or elevate shoulders on a bench."}
    ]
  },
  biceps: {
    gym: [
      {name:"Barbell/EZ-Bar Curl", sets:3, reps:"8–12", rest:"60–90 sec", tempo:"2-0-1-1",
       form:"Elbows pinned to sides, curl without swinging the torso.",
       mistake:"Using body momentum ('cheat curls') on every rep.",
       tip:"Squeeze at the top and control the lowering phase.",
       beginnerAlt:"Cable curl for constant tension with less stabilization demand.",
       advancedVar:"Drag curl or 21s technique."}
    ],
    home: [
      {name:"Dumbbell Curl (alternating)", sets:3, reps:"10–14", rest:"60 sec", tempo:"2-0-1-1",
       form:"Rotate palm up as you curl, keep elbow stationary.",
       mistake:"Letting the elbow drift forward.",
       tip:"Face a mirror or wall to self-check elbow position.",
       beginnerAlt:"Seated to remove swing.",
       advancedVar:"Incline dumbbell curl for a longer stretch."}
    ],
    bodyweight: [
      {name:"Band Curl", sets:3, reps:"12–20", rest:"60 sec", tempo:"2-0-1-1",
       form:"Stand on band, curl hands to shoulders, elbows fixed.",
       mistake:"Flaring elbows out to the sides.",
       tip:"Choke up on the band for more resistance as it shortens.",
       beginnerAlt:"Lighter band tension.",
       advancedVar:"Slow negative (4-sec lowering)."}
    ]
  },
  triceps: {
    gym: [
      {name:"Cable Triceps Pushdown", sets:3, reps:"10–15", rest:"60–90 sec", tempo:"2-0-1-1",
       form:"Elbows pinned at sides, extend fully, control the return.",
       mistake:"Letting elbows drift forward and using shoulders.",
       tip:"Lean slightly forward and keep elbows glued to ribs.",
       beginnerAlt:"Assisted machine dip.",
       advancedVar:"Overhead cable triceps extension for long-head emphasis."}
    ],
    home: [
      {name:"Dumbbell Overhead Triceps Extension", sets:3, reps:"10–15", rest:"60 sec", tempo:"2-0-1-1",
       form:"Both hands on one dumbbell overhead, lower behind head, extend fully.",
       mistake:"Flaring elbows out wide.",
       tip:"Keep elbows pointing forward, close to your ears.",
       beginnerAlt:"Two-hand support with lighter weight.",
       advancedVar:"Single-arm version."}
    ],
    bodyweight: [
      {name:"Close-Grip / Bench Dip", sets:3, reps:"10–20", rest:"60–90 sec", tempo:"2-0-1-1",
       form:"Hands close together (push-up) or behind on bench (dip), elbows track back.",
       mistake:"Letting elbows flare wide.",
       tip:"Keep torso rigid, no sagging hips.",
       beginnerAlt:"Bent-knee bench dips or incline close-grip push-ups.",
       advancedVar:"Feet elevated bench dips."}
    ]
  },
  forearms: {
    gym: [
      {name:"Barbell Wrist Curl", sets:3, reps:"15–20", rest:"45–60 sec", tempo:"2-0-1-1",
       form:"Forearms on bench/thighs, curl wrists up through full range.",
       mistake:"Using too much weight and only moving a few inches.",
       tip:"Slow the lowering phase for a deeper stretch.",
       beginnerAlt:"Lighter dumbbells one arm at a time.",
       advancedVar:"Reverse wrist curl added for extensors."}
    ],
    home: [
      {name:"Dumbbell Wrist Curl / Farmer's Carry", sets:3, reps:"15–20 or 40m walk", rest:"60 sec", tempo:"controlled",
       form:"For carries: stand tall, shoulders back, walk with dumbbells at sides.",
       mistake:"Letting shoulders round forward during carries.",
       tip:"Grip as hard as possible throughout the set.",
       beginnerAlt:"Shorter carry distance.",
       advancedVar:"Heavier load, single-arm carry for core anti-lateral-flexion."}
    ],
    bodyweight: [
      {name:"Dead Hang", sets:3, reps:"20–40 sec", rest:"60 sec", tempo:"hold",
       form:"Hang from a bar with relaxed shoulders, full grip.",
       mistake:"Shrugging shoulders to ears the whole time.",
       tip:"Actively pull shoulder blades down slightly ('active hang') for part of the set.",
       beginnerAlt:"Use a resistance band for foot support to reduce bodyweight.",
       advancedVar:"One-arm dead hang for short intervals."}
    ]
  },
  traps: {
    gym: [
      {name:"Barbell/DB Shrug", sets:3, reps:"12–15", rest:"60–90 sec", tempo:"2-1-1-1",
       form:"Lift shoulders straight up toward ears, pause, lower with control.",
       mistake:"Rolling shoulders in circles, which can irritate the joint.",
       tip:"Straight up and down motion only, squeeze at the top.",
       beginnerAlt:"Lighter dumbbells.",
       advancedVar:"Pause shrug with 2-second hold at top."}
    ],
    home: [
      {name:"Dumbbell Shrug", sets:3, reps:"12–15", rest:"60 sec", tempo:"2-1-1-1",
       form:"Arms straight at sides, elevate shoulders directly upward.",
       mistake:"Using the biceps to help lift.",
       tip:"Keep a light bend in elbows, focus purely on the traps.",
       beginnerAlt:"Lighter dumbbells or one arm at a time.",
       advancedVar:"Slow 3-second lowering phase."}
    ],
    bodyweight: [
      {name:"Band Shrug", sets:3, reps:"15–20", rest:"45–60 sec", tempo:"2-1-1-1",
       form:"Stand on band, elevate shoulders straight up against tension.",
       mistake:"Bending elbows to help lift.",
       tip:"Choke up on the band for more resistance.",
       beginnerAlt:"Lighter band.",
       advancedVar:"Add a 2-second peak hold."}
    ]
  },
  abs: {
    gym: [
      {name:"Cable Crunch", sets:3, reps:"12–15", rest:"60 sec", tempo:"2-0-1-1",
       form:"Kneel below cable, curl torso down by flexing the spine, not pulling with arms.",
       mistake:"Pulling with arms instead of crunching the spine.",
       tip:"Exhale fully as you crunch down to deepen the contraction.",
       beginnerAlt:"Bodyweight crunch instead.",
       advancedVar:"Weighted decline sit-up."}
    ],
    home: [
      {name:"Weighted Plank / Dumbbell Sit-Up", sets:3, reps:"30–45 sec or 12–15 reps", rest:"45–60 sec", tempo:"controlled",
       form:"Plank: straight line, brace like being punched. Sit-up: control both directions.",
       mistake:"Letting hips sag in plank or using momentum in sit-ups.",
       tip:"Squeeze glutes during planks to protect the lower back.",
       beginnerAlt:"Shorter hold time or knee plank.",
       advancedVar:"Add a weight plate on the chest."}
    ],
    bodyweight: [
      {name:"Plank / Bicycle Crunch", sets:3, reps:"30–45 sec or 15–20 reps", rest:"45–60 sec", tempo:"controlled",
       form:"Plank: neutral spine, core braced. Bicycle: rotate elbow to opposite knee with control.",
       mistake:"Rushing bicycle crunches without full rotation.",
       tip:"Slow the tempo — abs respond well to controlled time under tension.",
       beginnerAlt:"Dead bug variation for a gentler core intro.",
       advancedVar:"Hollow body hold or hanging leg raise."}
    ]
  },
  calves: {
    gym: [
      {name:"Standing/Seated Calf Raise", sets:4, reps:"12–20", rest:"45–60 sec", tempo:"2-1-1-1",
       form:"Full stretch at bottom, rise onto toes, pause and squeeze at top.",
       mistake:"Bouncing quickly without a full range of motion.",
       tip:"Pause for 1–2 seconds at the top of every rep.",
       beginnerAlt:"Bodyweight calf raise first.",
       advancedVar:"Single-leg calf raise."}
    ],
    home: [
      {name:"Dumbbell Calf Raise (step edge)", sets:4, reps:"15–20", rest:"45–60 sec", tempo:"2-1-1-1",
       form:"Stand on a step, heels drop below edge, rise onto toes fully.",
       mistake:"Not using a full range of motion.",
       tip:"Hold a wall or rail for balance so you can focus on the calf contraction.",
       beginnerAlt:"Both feet, no added weight.",
       advancedVar:"Single-leg version with dumbbell."}
    ],
    bodyweight: [
      {name:"Standing Calf Raise", sets:4, reps:"20–25", rest:"45 sec", tempo:"2-1-1-1",
       form:"Rise onto toes as high as possible, lower with control past neutral.",
       mistake:"Rushing through reps with tiny range of motion.",
       tip:"Do these on a step for a deeper stretch at the bottom.",
       beginnerAlt:"Both feet, hold onto wall for balance.",
       advancedVar:"Single-leg calf raise, slow tempo."}
    ]
  }
};

/* Split day-type -> muscle group focus mapping */
const DAY_FOCUS = {
  "Full Body": ["chest","back","legs","shoulders","abs"],
  "Push": ["chest","shoulders","triceps"],
  "Pull": ["back","biceps","traps"],
  "Legs": ["legs","glutes","calves"],
  "Upper": ["chest","back","shoulders","biceps","triceps"],
  "Lower": ["legs","glutes","calves","abs"],
  "Chest & Triceps": ["chest","triceps"],
  "Back & Biceps": ["back","biceps"],
  "Shoulders & Traps": ["shoulders","traps"],
  "Arms & Forearms": ["biceps","triceps","forearms"],
  "Glutes & Core": ["glutes","abs","calves"]
};

function getSplitPlan(days, experience){
  days = parseInt(days,10);
  if(days <= 2) return {name:"Full Body", days:Array(days).fill("Full Body")};
  if(days === 3){
    if(experience === "beginner") return {name:"Full Body ×3", days:["Full Body","Full Body","Full Body"]};
    return {name:"Push / Pull / Legs", days:["Push","Pull","Legs"]};
  }
  if(days === 4) return {name:"Upper / Lower", days:["Upper","Lower","Upper","Lower"]};
  if(days === 5){
    if(experience === "advanced") return {name:"Bro Split", days:["Chest & Triceps","Back & Biceps","Shoulders & Traps","Legs","Arms & Forearms"]};
    return {name:"PPL + Upper/Lower", days:["Push","Pull","Legs","Upper","Lower"]};
  }
  return {name:"Push / Pull / Legs ×2", days:["Push","Pull","Legs","Push","Pull","Legs"]};
}

function pickExercises(muscle, equipment, count){
  const bank = (EX[muscle] && (EX[muscle][equipment] || EX[muscle].bodyweight)) || [];
  return bank.slice(0, count);
}

function buildWorkout(state){
  const split = getSplitPlan(state.days, state.experience);
  const perMuscleCount = state.time <= 30 ? 1 : (state.time <= 45 ? 2 : 2);
  return split.days.map((focus, i) => {
    const muscles = DAY_FOCUS[focus];
    let exercises = [];
    muscles.forEach(m => {
      exercises = exercises.concat(pickExercises(m, state.equipment, perMuscleCount));
    });
    return {dayNum: i+1, focus, exercises};
  }).map(d => ({...d, splitName: split.name}));
}

/* =========================================================
   NUTRITION DATA — Indian-forward, adaptable meal library
   ========================================================= */
const MEALS = {
  veg: {
    breakfast: ["Vegetable poha with peanuts + a glass of milk","Besan chilla (2) with mint chutney + curd","Moong dal cheela with paneer stuffing","Oats porridge with milk, banana and almonds"],
    lunch: ["2 roti + paneer bhurji + dal + salad","Rajma + brown rice + cucumber raita","Chole + 1 roti + salad + curd","Mixed vegetable + soya chunk curry + rice"],
    dinner: ["Paneer tikka + sautéed vegetables + 1 roti","Dal tadka + roti + stir-fried greens","Vegetable khichdi with ghee + curd","Tofu/paneer stir-fry + quinoa"],
    snacks: ["Roasted chana + fruit","Greek yogurt with nuts","Sprouts chaat","Boiled eggs are non-veg — swap for paneer cubes with chaat masala"],
    pre: ["Banana with peanut butter","Handful of dates + black coffee","Poha or a small bowl of oats (60–90 min before)"],
    post: ["Paneer bhurji + roti","Whey protein shake with banana","Greek yogurt with honey and fruit","Moong dal chilla"]
  },
  vegan: {
    breakfast: ["Vegetable poha with peanuts (no ghee)","Tofu bhurji with vegetables","Oats with soy milk, chia seeds and banana","Moong dal cheela (oil, no dairy)"],
    lunch: ["Chickpea curry + brown rice + salad","Rajma + roti (no ghee) + salad","Tofu + mixed vegetable curry + rice","Lentil soup + quinoa + steamed greens"],
    dinner: ["Tofu stir-fry + quinoa","Dal tadka (no ghee) + roti + sautéed greens","Chickpea/vegetable khichdi","Tempeh or soy chunk curry + rice"],
    snacks: ["Roasted chana", "Trail mix (nuts + seeds)","Fruit with peanut butter","Hummus with cucumber and carrot sticks"],
    pre: ["Banana with peanut butter","Dates + black coffee","Small bowl of oats with soy milk"],
    post: ["Soy/pea protein shake with banana","Tofu bhurji + roti","Lentil soup with quinoa","Roasted chickpeas + fruit"]
  },
  nonveg: {
    breakfast: ["3 egg whites + 1 whole egg omelette + toast","Chicken sausage + oats","Boiled eggs (2–3) + fruit + milk","Egg bhurji with vegetables + roti"],
    lunch: ["Grilled chicken breast + rice + dal + salad","Fish curry + brown rice + sautéed greens","Chicken curry + 1 roti + salad","Egg curry + rice + vegetables"],
    dinner: ["Grilled fish/chicken + quinoa + vegetables","Chicken stir-fry + brown rice","Egg bhurji + roti + salad","Prawn curry + rice + greens"],
    snacks: ["Boiled eggs + fruit","Greek yogurt with nuts","Roasted chana","Chicken tikka pieces"],
    pre: ["Banana with peanut butter","Boiled egg + toast","Black coffee + dates"],
    post: ["Whey protein shake + banana","Grilled chicken + rice","Egg whites + toast","Greek yogurt with honey"]
  }
};

const HIGH_PROTEIN = {
  veg: ["Paneer","Greek yogurt","Milk","Tofu","Lentils (dal)","Chickpeas","Rajma","Soy chunks","Quinoa","Nuts & seeds"],
  vegan: ["Tofu","Tempeh","Lentils","Chickpeas","Rajma","Soy milk","Soy chunks","Quinoa","Peanut butter","Seitan"],
  nonveg: ["Eggs","Chicken breast","Fish","Prawns","Paneer","Greek yogurt","Milk","Lentils","Chickpeas","Quinoa"]
};

function calcTargets(state){
  const {age, gender, height, weight, activity, goal} = state;
  let bmr = gender === "male"
    ? 10*weight + 6.25*height - 5*age + 5
    : 10*weight + 6.25*height - 5*age - 161;
  const tdee = bmr * parseFloat(activity);

  let calorieTarget, proteinPerKg, note;
  switch(goal){
    case "fatloss": calorieTarget = tdee * 0.80; proteinPerKg = 2.0; note="~20% calorie deficit for steady, sustainable fat loss (~0.5–0.75 kg/week)."; break;
    case "musclegain": calorieTarget = tdee * 1.12; proteinPerKg = 1.8; note="~12% calorie surplus to support lean muscle gain while minimizing fat gain."; break;
    case "strength": calorieTarget = tdee * 1.05; proteinPerKg = 1.8; note="Slight surplus to fuel heavy, progressive strength work."; break;
    case "recomp": calorieTarget = tdee; proteinPerKg = 2.2; note="Calories at maintenance with high protein — build muscle and lose fat slowly at once."; break;
    default: calorieTarget = tdee; proteinPerKg = 1.6; note="Calories at maintenance to support performance and general health.";
  }
  const protein = proteinPerKg * weight;
  const fat = (calorieTarget * 0.25) / 9;
  const carbs = (calorieTarget - (protein*4) - (fat*9)) / 4;
  const bmi = weight / ((height/100)*(height/100));
  const water = (weight * 0.035).toFixed(1);

  return {
    bmr: Math.round(bmr), tdee: Math.round(tdee), calorieTarget: Math.round(calorieTarget),
    protein: Math.round(protein), fat: Math.round(fat), carbs: Math.round(carbs),
    bmi: bmi.toFixed(1), water, note
  };
}

/* =========================================================
   FORM NAVIGATION
   ========================================================= */
let currentRound = 1;
function updatePlateTrack(){
  for(let i=1;i<=3;i++){
    const p = document.getElementById('plate-'+i);
    p.classList.remove('active','done');
    if(i < currentRound) p.classList.add('done');
    else if(i === currentRound) p.classList.add('active');
  }
  document.getElementById('plateLabel').textContent = "ROUND "+currentRound+" OF 3";
}
function showRound(n){
  document.querySelectorAll('.round').forEach(r => {
    r.style.display = (parseInt(r.dataset.round,10) === n) ? 'block' : 'none';
  });
  currentRound = n;
  updatePlateTrack();
}
function nextRound(from){
  if(from === 1){
    const age = document.getElementById('age').value;
    const height = document.getElementById('height').value;
    const weight = document.getElementById('weight').value;
    const err = document.getElementById('err1');
    if(!age || !height || !weight){ err.style.display = 'block'; return; }
    err.style.display = 'none';
  }
  showRound(from+1);
  document.getElementById('assessment').scrollIntoView({behavior:'smooth', block:'start'});
}
function prevRound(from){ showRound(from-1); }

// Initialize plate indicators
document.addEventListener('DOMContentLoaded', () => {
  updatePlateTrack();
});

/* =========================================================
   FORM SUBMIT -> GENERATE PLAN
   ========================================================= */
let activeState = null; // Holds calculations state globally
document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('assessForm');
  if(form) {
    form.addEventListener('submit', function(e){
      e.preventDefault();
      const state = {
        age: parseFloat(document.getElementById('age').value) || 25,
        gender: document.querySelector('input[name=gender]:checked').value,
        height: parseFloat(document.getElementById('height').value) || 170,
        weight: parseFloat(document.getElementById('weight').value) || 70,
        goal: document.querySelector('input[name=goal]:checked').value,
        activity: document.querySelector('input[name=activity]:checked').value,
        experience: document.querySelector('input[name=experience]:checked').value,
        equipment: document.querySelector('input[name=equipment]:checked').value,
        diet: document.querySelector('input[name=diet]:checked').value,
        allergies: document.getElementById('allergies').value.trim(),
        days: document.getElementById('days').value,
        time: parseInt(document.getElementById('time').value,10)
      };
      activeState = state;
      renderPlan(state);
      document.getElementById('results').style.display = 'block';
      document.getElementById('results').scrollIntoView({behavior:'smooth', block:'start'});
    });
  }
});

const GOAL_LABEL = {fatloss:"Fat loss", musclegain:"Muscle gain", strength:"Strength", recomp:"Body recomposition", general:"General fitness"};
const DIET_LABEL = {veg:"Vegetarian", vegan:"Vegan", nonveg:"Non-vegetarian"};

function renderPlan(state){
  const t = calcTargets(state);
  const split = getSplitPlan(state.days, state.experience);
  const workout = buildWorkout(state);

  document.getElementById('planTitle').textContent = GOAL_LABEL[state.goal] + " — " + split.name;

  // Stat row
  document.getElementById('statRow').innerHTML = `
    <div class="stat animate-fade-up"><div class="label">Calorie target</div><div class="num">${t.calorieTarget}<span class="unit">kcal/day</span></div></div>
    <div class="stat animate-fade-up" style="animation-delay: 0.1s"><div class="label">Protein</div><div class="num">${t.protein}<span class="unit">g/day</span></div></div>
    <div class="stat animate-fade-up" style="animation-delay: 0.2s"><div class="label">BMI</div><div class="num">${t.bmi}</div></div>
    <div class="stat animate-fade-up" style="animation-delay: 0.3s"><div class="label">Split</div><div class="num" style="font-size:18px;color:var(--color-success)">${split.name}</div></div>
  `;

  // Dynamic Heart Rate Zones Calculation
  const maxHR = 220 - state.age;
  const hrZones = {
    z1: { min: Math.round(maxHR * 0.5), max: Math.round(maxHR * 0.6) }, // Warm up
    z2: { min: Math.round(maxHR * 0.6), max: Math.round(maxHR * 0.7) }, // Fat Burn
    z3: { min: Math.round(maxHR * 0.7), max: Math.round(maxHR * 0.8) }, // Cardio
    z4: { min: Math.round(maxHR * 0.8), max: Math.round(maxHR * 0.9) }  // Peak
  };

  // Dynamic Water Logger Variables
  const targetGlasses = Math.round(t.water * 4); // 250ml per glass
  const savedWaterCount = parseInt(localStorage.getItem(`water_log_${today()}`) || '0', 10);

  // Overview tab HTML
  let allergyNote = "";
  if(state.allergies){
    allergyNote = `<div class="disclaimer" style="margin-top:20px;"><strong>Noted:</strong> you mentioned "${escapeHtml(state.allergies)}". Swap any listed foods or exercises that conflict with this, and check with a healthcare professional if it involves an injury or diagnosed condition.</div>`;
  }
  document.getElementById('tab-overview').innerHTML = `
    <div class="meal-card">
      <h4>Metabolic snapshot</h4>
      <table>
        <tr><td>BMR (calories at rest)</td><td class="mono">${t.bmr} kcal</td></tr>
        <tr><td>TDEE (maintenance calories)</td><td class="mono">${t.tdee} kcal</td></tr>
        <tr><td>Daily calorie target</td><td class="mono">${t.calorieTarget} kcal</td></tr>
        <tr><td>Protein</td><td class="mono">${t.protein} g</td></tr>
        <tr><td>Carbohydrates</td><td class="mono">${t.carbs} g</td></tr>
        <tr><td>Fat</td><td class="mono">${t.fat} g</td></tr>
        <tr><td>Hydration target</td><td class="mono">${t.water} L/day (more on training days)</td></tr>
      </table>
      <p style="color:var(--text-secondary);font-size:13px;margin-top:14px;">${t.note}</p>
    </div>

    <!-- HEART RATE ZONE WIDGET -->
    <div class="meal-card">
      <h4>Heart Rate Training Zones</h4>
      <p style="color:var(--text-secondary);font-size:13px;margin-bottom:14px;">Optimized targets based on your age (${state.age}):</p>
      <div class="hr-zone-grid">
        <div class="hr-zone-card z1">
          <h5>Zone 1: Warm Up (50-60%)</h5>
          <p>Mobility & Active recovery</p>
          <div class="bpm">${hrZones.z1.min} – ${hrZones.z1.max} BPM</div>
        </div>
        <div class="hr-zone-card z2">
          <h5>Zone 2: Fat Burn (60-70%)</h5>
          <p>Aerobic base development</p>
          <div class="bpm">${hrZones.z2.min} – ${hrZones.z2.max} BPM</div>
        </div>
        <div class="hr-zone-card z3">
          <h5>Zone 3: Cardio (70-80%)</h5>
          <p>Aerobic endurance & capacity</p>
          <div class="bpm">${hrZones.z3.min} – ${hrZones.z3.max} BPM</div>
        </div>
        <div class="hr-zone-card z4">
          <h5>Zone 4: Peak (80-90%)</h5>
          <p>Anaerobic speed & power</p>
          <div class="bpm">${hrZones.z4.min} – ${hrZones.z4.max} BPM</div>
        </div>
      </div>
    </div>

    <!-- WATER LOGGER WIDGET -->
    <div class="meal-card">
      <h4>Daily Hydration Logger</h4>
      <p style="color:var(--text-secondary);font-size:13px;margin-bottom:16px;">Aim for ${t.water} L (${targetGlasses} glasses of 250ml each). Click on glasses to log consumption:</p>
      <div class="water-tracker-container">
        <div class="water-glasses" id="waterGlassesGrid"></div>
        <div style="font-size: 14px; font-weight: 600;" id="waterCountLabel">${savedWaterCount} / ${targetGlasses} glasses</div>
        <div class="water-progress-bar">
          <div class="water-progress-fill" id="waterProgressFill"></div>
        </div>
      </div>
    </div>

    ${allergyNote}
    <div class="disclaimer">
      <strong>Reminder:</strong> if you have a diagnosed medical condition, injury, or are pregnant, consult a qualified healthcare professional before starting this or any program.
    </div>
  `;

  // Draw initial water glasses
  drawWaterTracker(savedWaterCount, targetGlasses);

  // Workout tab HTML
  document.getElementById('tab-workout').innerHTML = workout.map(d => `
    <div class="day-card">
      <div class="day-head">
        <span class="name">Day ${d.dayNum}</span>
        <span class="focus">${d.focus}</span>
      </div>
      <table>
        <thead><tr><th>Exercise</th><th>Sets</th><th>Reps</th><th>Rest</th><th>Tempo</th></tr></thead>
        <tbody>
          ${d.exercises.map(ex => `<tr><td>${ex.name}</td><td class="mono">${ex.sets}</td><td class="mono">${ex.reps}</td><td class="mono">${ex.rest}</td><td class="mono">${ex.tempo}</td></tr>`).join('')}
        </tbody>
      </table>
      ${d.exercises.map(ex => `
        <details>
          <summary>${ex.name} — form, mistakes &amp; variations</summary>
          <div class="ex-detail">
            <div><span class="k">Proper form</span>${ex.form}</div>
            <div class="row2">
              <div><span class="k">Common mistake</span>${ex.mistake}</div>
              <div><span class="k">Coaching tip</span>${ex.tip}</div>
            </div>
            <div class="row2">
              <div><span class="k">Beginner alternative</span>${ex.beginnerAlt}</div>
              <div><span class="k">Advanced variation</span>${ex.advancedVar}</div>
            </div>
          </div>
        </details>
      `).join('')}
    </div>
  `).join('') + `<p style="color:var(--text-muted);font-size:13px;">Rest 1–2 full days between sessions hitting the same muscle group. Warm up with 5 minutes of light cardio plus 1–2 light warm-up sets before your first working set of each exercise.</p>`;

  // Nutrition tab HTML
  const m = MEALS[state.diet];
  document.getElementById('tab-nutrition').innerHTML = `
    <div class="meal-card">
      <h4>Sample day — ${DIET_LABEL[state.diet]}, ${GOAL_LABEL[state.goal]}</h4>
      <table>
        <tr><td style="width:140px;color:var(--text-secondary);">Breakfast</td><td>${pick(m.breakfast)}</td></tr>
        <tr><td style="color:var(--text-secondary);">Lunch</td><td>${pick(m.lunch)}</td></tr>
        <tr><td style="color:var(--text-secondary);">Evening snack</td><td>${pick(m.snacks)}</td></tr>
        <tr><td style="color:var(--text-secondary);">Dinner</td><td>${pick(m.dinner)}</td></tr>
      </table>
    </div>
    <div class="meal-card">
      <h4>Pre-workout (60–90 min before)</h4>
      <ul>${m.pre.map(x=>`<li>${x}</li>`).join('')}</ul>
    </div>
    <div class="meal-card">
      <h4>Post-workout (within 60 min after)</h4>
      <ul>${m.post.map(x=>`<li>${x}</li>`).join('')}</ul>
      <p style="color:var(--text-secondary);font-size:13px;margin-top:8px;">Aim for roughly ${Math.round(state.weight*0.3)}–${Math.round(state.weight*0.4)} g protein and a moderate portion of carbs in this meal to kick off recovery.</p>
    </div>
    <div class="meal-card">
      <h4>High-protein foods to build meals around</h4>
      <div class="food-chip-row">${HIGH_PROTEIN[state.diet].map(f=>`<span class="chip">${f}</span>`).join('')}</div>
    </div>
    <div class="meal-card">
      <h4>Weekly structure tip</h4>
      <p style="color:var(--text-primary);font-size:14px;">Rotate the breakfast/lunch/dinner options above across the week so meals stay varied while calories and protein stay consistent. Batch-cook dal, rice/quinoa, and a protein source (paneer, tofu, chicken, or eggs) every 2–3 days to save time.</p>
    </div>
  `;

  // Supplements tab HTML
  document.getElementById('tab-supplements').innerHTML = `
    <div class="supp-grid">
      <div class="supp-card"><span class="tag">Recovery</span><h4>Whey / Plant Protein</h4><p><strong>Use:</strong> convenient way to hit protein target.</p><p><strong>Dose:</strong> 20–30g per serving.</p><p><strong>Timing:</strong> anytime; post-workout is convenient, not mandatory.</p></div>
      <div class="supp-card"><span class="tag">Strength</span><h4>Creatine Monohydrate</h4><p><strong>Use:</strong> improves strength and power output.</p><p><strong>Dose:</strong> 3–5g daily, any time of day.</p><p><strong>Note:</strong> most researched supplement for strength training; drink enough water.</p></div>
      <div class="supp-card"><span class="tag">Foundation</span><h4>Multivitamin</h4><p><strong>Use:</strong> covers micronutrient gaps.</p><p><strong>Dose:</strong> per label, usually once daily with food.</p><p><strong>Note:</strong> not a replacement for whole foods.</p></div>
      <div class="supp-card"><span class="tag">Health</span><h4>Omega-3 (Fish/Algae Oil)</h4><p><strong>Use:</strong> supports heart and joint health.</p><p><strong>Dose:</strong> 1–2g combined EPA/DHA daily with a meal.</p></div>
      <div class="supp-card"><span class="tag">Health</span><h4>Vitamin D</h4><p><strong>Use:</strong> common deficiency with limited sun exposure.</p><p><strong>Dose:</strong> 1000–2000 IU daily, or as advised by a doctor after a blood test.</p></div>
      <div class="supp-card"><span class="tag">Hydration</span><h4>Electrolytes</h4><p><strong>Use:</strong> helpful during long or hot, sweaty sessions.</p><p><strong>Timing:</strong> during/after intense or 60+ minute workouts.</p></div>
      <div class="supp-card"><span class="tag">Performance</span><h4>Caffeine</h4><p><strong>Use:</strong> improves focus and performance.</p><p><strong>Dose:</strong> 100–200mg, 30–45 min pre-workout.</p><p><strong>Note:</strong> avoid late in the day if it affects sleep.</p></div>
      <div class="supp-card"><span class="tag">Optional</span><h4>BCAAs</h4><p><strong>Use:</strong> largely unnecessary if total daily protein is adequate.</p><p><strong>Note:</strong> whole protein sources or whey cover this better in most cases.</p></div>
    </div>
    <div class="disclaimer" style="margin-top:20px;">
      <strong>Supplements are optional.</strong> Whole foods should always be your primary source of nutrition — supplements fill small gaps, they don't replace meals. Check with a doctor before starting any supplement if you have a medical condition or take medication.
    </div>
  `;

  // Progress tab HTML
  document.getElementById('tab-progress').innerHTML = `
    <!-- WEEKLY WORKOUT TRACKER CALENDAR -->
    <div class="meal-card animate-fade-up">
      <h4>Weekly Workout Tracker Checklist</h4>
      <p style="color:var(--text-secondary);font-size:13px;margin-bottom:12px;">Check off days when you complete a workout to build your weekly streak:</p>
      <div class="workout-calendar-grid" id="weeklyWorkoutGrid"></div>
      <div style="margin-top: 16px; font-size: 14px; font-weight: 600;" id="workoutStreakLabel">Streaks logged this week: 0 days</div>
    </div>

    <!-- LOG ENTRIES -->
    <div class="meal-card">
      <h4>Log a check-in</h4>
      <div class="log-form">
        <div class="field"><label for="logDate">Date</label><input type="text" id="logDate" placeholder="e.g. Week 1"></div>
        <div class="field"><label for="logWeight">Weight (kg)</label><input type="number" id="logWeight" step="0.1"></div>
        <div class="field"><label for="logNote">Note</label><input type="text" id="logNote" placeholder="energy, sleep, strength PRs..."></div>
        <button class="btn small" type="button" onclick="addLog()">Add entry</button>
      </div>
      <table id="logTable">
        <thead><tr><th>Date</th><th>Weight (kg)</th><th>Note</th></tr></thead>
        <tbody id="logBody"></tbody>
      </table>
      <p style="color:var(--text-muted);font-size:12px;margin-top:16px;">This log lives only in your current browser session — it resets on reload. Track weekly, at the same time of day, for the most reliable trend.</p>
    </div>
    <div class="meal-card">
      <h4>What to track weekly</h4>
      <ul>
        <li>Body weight (same day/time each week — not daily, weight fluctuates naturally)</li>
        <li>Key lift numbers (weight × reps on your main compound movements)</li>
        <li>Workout consistency (sessions completed vs. planned)</li>
        <li>Sleep hours and quality</li>
        <li>How clothes fit / progress photos (optional, monthly)</li>
      </ul>
    </div>
  `;

  // Draw initial workout tracker days
  drawWorkoutTracker();

  logEntries.length = 0;
  renderLog();
}

/* =========================================================
   NEW FEATURE FUNCTIONS
   ========================================================= */

// 1. Water Intake Logger
function drawWaterTracker(current, target) {
  const grid = document.getElementById('waterGlassesGrid');
  if(!grid) return;
  
  let html = '';
  for(let i = 1; i <= target; i++) {
    const activeClass = i <= current ? 'active' : '';
    html += `<div class="water-glass ${activeClass}" onclick="toggleWaterGlass(${i})"></div>`;
  }
  grid.innerHTML = html;
  
  // Fill progress bar
  const progressPercent = Math.min((current / target) * 100, 100);
  const fill = document.getElementById('waterProgressFill');
  if(fill) fill.style.width = `${progressPercent}%`;
}

window.toggleWaterGlass = function(index) {
  if(!activeState) return;
  const t = calcTargets(activeState);
  const target = Math.round(t.water * 4);
  const dateKey = `water_log_${today()}`;
  let current = parseInt(localStorage.getItem(dateKey) || '0', 10);
  
  // Toggle glass count
  if(index === current) {
    current = index - 1; // back down
  } else {
    current = index; // advance
  }
  if(current < 0) current = 0;
  
  localStorage.setItem(dateKey, current);
  
  // Update labels
  const label = document.getElementById('waterCountLabel');
  if(label) label.textContent = `${current} / ${target} glasses`;
  
  drawWaterTracker(current, target);
};

// 2. Weekly Workout Tracker
const WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

function drawWorkoutTracker() {
  const grid = document.getElementById('weeklyWorkoutGrid');
  if(!grid) return;

  const currentChecks = JSON.parse(localStorage.getItem('workoutStreak_v1') || '[]');
  
  let html = '';
  WEEKDAYS.forEach(day => {
    const isCompleted = currentChecks.includes(day);
    const completedClass = isCompleted ? 'completed' : '';
    html += `
      <div class="workout-day-box ${completedClass}" onclick="toggleWorkoutDay('${day}')">
        <div class="day-name">${day}</div>
        <div class="check-indicator"></div>
      </div>
    `;
  });
  grid.innerHTML = html;
  
  // Update streak count
  const label = document.getElementById('workoutStreakLabel');
  if(label) label.textContent = `Completed workouts this week: ${currentChecks.length} day(s)`;
}

window.toggleWorkoutDay = function(day) {
  let currentChecks = JSON.parse(localStorage.getItem('workoutStreak_v1') || '[]');
  const index = currentChecks.indexOf(day);
  if(index > -1) {
    currentChecks.splice(index, 1); // remove
  } else {
    currentChecks.push(day); // add
  }
  
  localStorage.setItem('workoutStreak_v1', JSON.stringify(currentChecks));
  drawWorkoutTracker();
};


/* Standard pick/escape functions */
function pick(arr){ return arr[Math.floor(Math.random()*arr.length)]; }
function escapeHtml(s){ return s.replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }

/* Tabs */
document.addEventListener('click', function(e){
  if(e.target.matches('.tab-btn')){
    document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));
    document.querySelectorAll('.tab-panel').forEach(p=>p.classList.remove('active'));
    e.target.classList.add('active');
    document.getElementById('tab-'+e.target.dataset.tab).classList.add('active');
  }
});

/* Progress log */
let logEntries = [];
function addLog(){
  const date = document.getElementById('logDate').value || ('Entry '+(logEntries.length+1));
  const weight = document.getElementById('logWeight').value || '—';
  const note = document.getElementById('logNote').value || '';
  logEntries.push({date, weight, note});
  document.getElementById('logDate').value = '';
  document.getElementById('logWeight').value = '';
  document.getElementById('logNote').value = '';
  renderLog();
}
function renderLog(){
  const body = document.getElementById('logBody');
  if(!body) return;
  body.innerHTML = logEntries.map(e=>`<tr><td>${escapeHtml(e.date)}</td><td class="mono">${e.weight}</td><td>${escapeHtml(e.note)}</td></tr>`).join('');
}

function today(){ return new Date().toISOString().slice(0,10); }

/* =========================================================
   FITNESS COMMUNITY HUB
   ========================================================= */
const CH = (function(){
  const STORE_KEY = 'chData_v1';

  function uid(){ return 'u'+Date.now().toString(36)+Math.random().toString(36).slice(2,7); }
  function todayDate(){ return today(); }
  function esc(s){ return typeof escapeHtml === 'function' ? escapeHtml(String(s||'')) : String(s||''); }
  
  function fileToDataUrl(file, cb){
    if(!file){ cb(null); return; }
    const r = new FileReader();
    r.onload = () => cb(r.result);
    r.onerror = () => cb(null);
    r.readAsDataURL(file);
  }

  const SEED_USERS = [
    {id:'seed1',name:'Rhea Kapoor',city:'Mumbai',age:27,gender:'female',goal:'fatloss',experience:'advanced',skills:['Nutrition','Fat Loss'],bio:'Coach helping people lose fat sustainably.',followers:[],following:[],badges:['Nutrition Expert'],availability:'Evenings'},
    {id:'seed2',name:'Vikram Singh',city:'Delhi',age:31,gender:'male',goal:'strength',experience:'advanced',skills:['Powerlifting','Strength'],bio:'Powerlifter, 5 years competitive.',followers:[],following:[],badges:['Coach'],availability:'Mornings'},
    {id:'seed3',name:'Ananya Rao',city:'Bengaluru',age:24,gender:'female',goal:'recomp',experience:'intermediate',skills:['Yoga','Calisthenics'],bio:'Yoga + bodyweight training enthusiast.',followers:[],following:[],badges:['Calisthenics Master'],availability:'Flexible'},
    {id:'seed4',name:'Karthik Iyer',city:'Vijayawada',age:29,gender:'male',goal:'musclegain',experience:'intermediate',skills:['Bodybuilding','Home Workouts'],bio:'Home-gym lifter, 3 years in.',followers:[],following:[],badges:['100 Workouts'],availability:'Weekends'},
    {id:'seed5',name:'Priya Menon',city:'Hyderabad',age:22,gender:'female',goal:'fatloss',experience:'beginner',skills:['Marathon Training'],bio:'Training for my first half marathon.',followers:[],following:[],badges:[],availability:'Evenings'}
  ];

  let data = load();

  function load(){
    try{
      const raw = localStorage.getItem(STORE_KEY);
      if(raw) return JSON.parse(raw);
    }catch(e){}
    return {currentUser:null, users:JSON.parse(JSON.stringify(SEED_USERS)), posts:[], questions:[], groups:[
      {id:'g1',name:'Weight Loss Group',desc:'Support and tips for fat loss.',members:[]},
      {id:'g2',name:'Muscle Gain Group',desc:'Bulking, hypertrophy, progressive overload.',members:[]},
      {id:'g3',name:'Beginners',desc:'New to fitness? Start here.',members:[]}
    ], challenges:[
      {id:'c1',name:'30-Day Push-up Challenge',desc:'Do push-ups daily for 30 days.',participants:{}},
      {id:'c2',name:'10,000 Steps Daily',desc:'Hit 10k steps every day this month.',participants:{}},
      {id:'c3',name:'Plank Challenge',desc:'Increase your plank hold every day.',participants:{}}
    ], messages:{}};
  }
  
  function save(){ 
    try{ 
      localStorage.setItem(STORE_KEY, JSON.stringify(data)); 
    }catch(e){ 
      console.error('CH storage error', e); 
    } 
  }

  function me(){ return data.currentUser; }
  function userById(id){ return data.users.find(u=>u.id===id); }

  function badgesFor(u){
    const b = new Set(u.badges||[]);
    const postCount = data.posts.filter(p=>p.userId===u.id).length;
    if(postCount>=1) b.add('Helpful Member');
    if(postCount>=5) b.add('Transformation Hero');
    return Array.from(b);
  }

  /* ---------------- ONBOARDING ---------------- */
  function join(){
    const name = document.getElementById('chName').value.trim();
    if(!name){ alert('Please enter a display name.'); return; }
    const city = document.getElementById('chCity').value.trim();
    const age = document.getElementById('chAge').value;
    const gender = document.querySelector('input[name=chGender]:checked').value;
    const goal = document.querySelector('input[name=chGoal]:checked').value;
    const skills = document.getElementById('chSkills').value.split(',').map(s=>s.trim()).filter(Boolean);
    
    const u = {id:uid(), name, city, age, gender, goal, experience:'beginner', skills, bio:'', height:'', weight:'', followers:[], following:[], badges:[], availability:''};
    data.users.push(u);
    data.currentUser = u.id;
    save();
    boot();
  }

  function boot(){
    if(!me()){
      document.getElementById('chOnboard').style.display = '';
      document.getElementById('chApp').style.display = 'none';
      return;
    }
    document.getElementById('chOnboard').style.display = 'none';
    document.getElementById('chApp').style.display = '';
    renderAll();
  }

  function renderAll(){
    renderFeed(); renderTransformations(); renderQuestions(); renderSkills();
    renderPartners(); renderGroups(); renderChallenges(); renderLeaderboard();
    renderChatUsers(); renderProfile();
  }

  /* ---------------- TABS ---------------- */
  document.addEventListener('DOMContentLoaded', () => {
    const tabsContainer = document.getElementById('chTabs');
    if(tabsContainer) {
      tabsContainer.addEventListener('click', function(e){
        if(!e.target.matches('.ch-tab-btn')) return;
        document.querySelectorAll('.ch-tab-btn').forEach(b=>b.classList.remove('active'));
        document.querySelectorAll('.ch-tab-panel').forEach(p=>p.classList.remove('active'));
        e.target.classList.add('active');
        document.getElementById('ch-'+e.target.dataset.ch).classList.add('active');
      });
    }
  });

  /* ---------------- POSTS / FEED / TRANSFORMATIONS ---------------- */
  function createPost(){
    const caption = document.getElementById('chCaption').value.trim();
    const beforeFile = document.getElementById('chBefore').files[0];
    const afterFile = document.getElementById('chAfter').files[0];
    const weightChange = document.getElementById('chWeightChange').value.trim();
    const timeTaken = document.getElementById('chTimeTaken').value.trim();
    if(!caption && !beforeFile && !afterFile){ alert('Add a caption or at least one photo.'); return; }
    
    fileToDataUrl(beforeFile, beforeImg => {
      fileToDataUrl(afterFile, afterImg => {
        const u = userById(me());
        data.posts.unshift({id:uid(), userId:u.id, caption, beforeImg, afterImg, weightChange, timeTaken, date:todayDate(), likes:[], comments:[]});
        save();
        document.getElementById('chCaption').value=''; document.getElementById('chWeightChange').value=''; document.getElementById('chTimeTaken').value='';
        document.getElementById('chBefore').value=''; document.getElementById('chAfter').value='';
        renderFeed(); renderTransformations(); renderLeaderboard();
      });
    });
  }

  function postCard(p){
    const u = userById(p.userId) || {name:'Deleted user'};
    const liked = p.likes.includes(me());
    const saved = (data.users.find(x=>x.id===me())||{}).bookmarks && data.users.find(x=>x.id===me()).bookmarks.includes(p.id);
    let ba = '';
    if(p.beforeImg || p.afterImg){
      ba = `<div class="ch-ba">
        <div>${p.beforeImg?`<img src="${p.beforeImg}">`:''}<div class="ch-ba-label">Before</div></div>
        <div>${p.afterImg?`<img src="${p.afterImg}">`:''}<div class="ch-ba-label">After</div></div>
      </div>`;
    }
    const meta = [p.weightChange, p.timeTaken].filter(Boolean).join(' · ');
    return `<div class="ch-card">
      <div class="ch-user-row"><div class="ch-avatar">${esc(u.name).charAt(0)}</div><div><div class="ch-username">${esc(u.name)}</div><div class="ch-meta">${p.date}</div></div></div>
      ${p.caption?`<p style="font-size:14px;color:var(--text-primary);">${esc(p.caption)}</p>`:''}
      ${ba}
      ${meta?`<div class="ch-meta" style="margin-top: 8px;">${esc(meta)}</div>`:''}
      <div class="ch-actions">
        <button class="ch-action ${liked?'liked':''}" onclick="CH.toggleLike('${p.id}')">♥ ${p.likes.length}</button>
        <button class="ch-action" onclick="CH.toggleComments('${p.id}')">💬 ${p.comments.length}</button>
        <button class="ch-action" onclick="CH.share('${p.id}')">↗ Share</button>
        <button class="ch-action ${saved?'saved':''}" onclick="CH.toggleSave('${p.id}')">🔖 ${saved?'Saved':'Save'}</button>
      </div>
      <div class="ch-comments" id="chComments-${p.id}">
        ${p.comments.map(c=>`<div class="ch-comment"><b>${esc(c.userName)}:</b> ${esc(c.text)}</div>`).join('')}
        <div class="ch-inline-form"><input type="text" id="chCommentInput-${p.id}" placeholder="Add a comment..."><button class="btn small" type="button" onclick="CH.addComment('${p.id}')">Post</button></div>
      </div>
    </div>`;
  }

  function renderFeed(){
    const el = document.getElementById('chFeedGrid');
    if(el) {
      el.innerHTML = data.posts.length ? data.posts.map(postCard).join('') : '<div class="ch-empty">No posts yet — be the first to share something.</div>';
    }
  }

  function renderTransformations(){
    const el = document.getElementById('chTransformGrid');
    if(el) {
      const list = data.posts.filter(p => p.beforeImg || p.afterImg);
      el.innerHTML = list.length ? list.map(postCard).join('') : '<div class="ch-empty">No transformations posted yet.</div>';
    }
  }

  function toggleLike(id){
    const p = data.posts.find(x=>x.id===id);
    const i = p.likes.indexOf(me());
    if(i>-1) p.likes.splice(i,1); else p.likes.push(me());
    save(); renderFeed(); renderTransformations(); renderLeaderboard();
  }

  function toggleComments(id){
    const c = document.getElementById('chComments-'+id);
    c.classList.toggle('open');
  }

  function addComment(id){
    const input = document.getElementById('chCommentInput-'+id);
    const text = input.value.trim(); if(!text) return;
    const p = data.posts.find(x=>x.id===id);
    p.comments.push({id:uid(), userId:me(), userName:userById(me()).name, text, date:todayDate()});
    input.value=''; save(); renderFeed(); renderTransformations();
    document.getElementById('chComments-'+id).classList.add('open');
  }

  function share(id){
    if(navigator.share){ 
      navigator.share({title:'Check out this post', url:location.href+'#community'}); 
    } else { 
      alert('Share link copied (demo): '+location.href+'#community'); 
    }
  }

  function toggleSave(id){
    const u = userById(me());
    u.bookmarks = u.bookmarks || [];
    const i = u.bookmarks.indexOf(id);
    if(i>-1) u.bookmarks.splice(i,1); else u.bookmarks.push(id);
    save(); renderFeed(); renderTransformations(); renderProfile();
  }

  /* ---------------- ASK COMMUNITY ---------------- */
  function askQuestion(){
    const input = document.getElementById('chQuestion');
    const text = input.value.trim(); if(!text) return;
    data.questions.unshift({id:uid(), userId:me(), userName:userById(me()).name, text, date:todayDate(), replies:[]});
    input.value=''; save(); renderQuestions();
  }

  function renderQuestions(){
    const el = document.getElementById('chQuestionList');
    if(el) {
      el.innerHTML = data.questions.length ? data.questions.map(q=>`
        <div class="ch-card" style="margin-bottom:20px;">
          <div class="ch-user-row"><div class="ch-avatar">${esc(q.userName).charAt(0)}</div><div><div class="ch-username">${esc(q.userName)}</div><div class="ch-meta">${q.date}</div></div></div>
          <p style="font-size:14px;color:var(--text-primary);">${esc(q.text)}</p>
          <div class="ch-comments open">
            ${q.replies.map(r=>`<div class="ch-comment"><b>${esc(r.userName)}:</b> ${esc(r.text)}</div>`).join('')}
            <div class="ch-inline-form"><input type="text" id="chReply-${q.id}" placeholder="Write a reply..."><button class="btn small" type="button" onclick="CH.replyQuestion('${q.id}')">Reply</button></div>
          </div>
        </div>`).join('') : '<div class="ch-empty">No questions yet — ask the community something.</div>';
    }
  }

  function replyQuestion(id){
    const input = document.getElementById('chReply-'+id);
    const text = input.value.trim(); if(!text) return;
    const q = data.questions.find(x=>x.id===id);
    q.replies.push({id:uid(), userId:me(), userName:userById(me()).name, text, date:todayDate()});
    input.value=''; save(); renderQuestions();
  }

  /* ---------------- SKILL EXCHANGE ---------------- */
  function userCard(u){
    const cur = userById(me());
    const following = cur && cur.following && cur.following.includes(u.id);
    const isMe = u.id === me();
    return `<div class="ch-card">
      <div class="ch-user-row"><div class="ch-avatar">${esc(u.name).charAt(0)}</div><div><div class="ch-username">${esc(u.name)}</div><div class="ch-meta">${esc(u.city||'')} ${u.age?'· '+u.age:''}</div></div></div>
      ${u.bio?`<p style="font-size:13px;color:var(--text-secondary);margin-bottom:8px;">${esc(u.bio)}</p>`:''}
      ${(u.skills||[]).map(s=>`<span class="ch-skill-chip">${esc(s)}</span>`).join('')}
      ${badgesFor(u).map(b=>`<span class="ch-badge">${esc(b)}</span>`).join('')}
      <div class="ch-meta" style="margin-top:8px;">${u.experience||''} ${u.availability?' · '+esc(u.availability):''}</div>
      <div class="ch-actions">
        ${!isMe?`<button class="ch-action ${following?'liked':''}" onclick="CH.toggleFollow('${u.id}')">${following?'✓ Following':'+ Follow'}</button>`:''}
        ${!isMe?`<button class="ch-action" onclick="CH.openChat('${u.id}')">✉ Message</button>`:''}
      </div>
    </div>`;
  }

  function renderSkills(){
    const el = document.getElementById('chSkillsGrid');
    if(el) {
      el.innerHTML = data.users.map(u=>userCard(u)).join('');
    }
  }

  // Toggle follow
  function toggleFollow(id){
    const cur = userById(me());
    cur.following = cur.following||[];
    const target = userById(id);
    target.followers = target.followers||[];
    const i = cur.following.indexOf(id);
    if(i>-1){ 
      cur.following.splice(i,1); 
      target.followers.splice(target.followers.indexOf(me()),1); 
    } else { 
      cur.following.push(id); 
      target.followers.push(me()); 
    }
    save(); renderSkills(); renderPartners(); renderProfile();
  }

  /* ---------------- FIND PARTNER ---------------- */
  function renderPartners(){
    const cityInput = document.getElementById('chFCity');
    const goalSelect = document.getElementById('chFGoal');
    const expSelect = document.getElementById('chFExp');
    
    const city = cityInput ? cityInput.value.toLowerCase() : '';
    const goal = goalSelect ? goalSelect.value : '';
    const exp = expSelect ? expSelect.value : '';
    
    const list = data.users.filter(u=>u.id!==me())
      .filter(u=> !city || (u.city||'').toLowerCase().includes(city))
      .filter(u=> !goal || u.goal===goal)
      .filter(u=> !exp || u.experience===exp);
      
    const el = document.getElementById('chPartnerGrid');
    if(el) {
      el.innerHTML = list.length ? list.map(u=>userCard(u)).join('') : '<div class="ch-empty">No matching partners. Try different filters.</div>';
    }
  }

  /* ---------------- GROUPS ---------------- */
  function createGroup(){
    const name = document.getElementById('chGroupName').value.trim();
    const desc = document.getElementById('chGroupDesc').value.trim();
    if(!name) return;
    data.groups.push({id:uid(), name, desc, members:[me()]});
    document.getElementById('chGroupName').value=''; document.getElementById('chGroupDesc').value='';
    save(); renderGroups();
  }

  function toggleGroupJoin(id){
    const g = data.groups.find(x=>x.id===id);
    const i = g.members.indexOf(me());
    if(i>-1) g.members.splice(i,1); else g.members.push(me());
    save(); renderGroups();
  }

  function renderGroups(){
    const el = document.getElementById('chGroupsGrid');
    if(el) {
      el.innerHTML = data.groups.map(g=>{
        const joined = g.members.includes(me());
        return `<div class="ch-card">
          <div class="ch-username">${esc(g.name)}</div>
          <p style="font-size:13px;color:var(--text-secondary);margin:8px 0;">${esc(g.desc)}</p>
          <div class="ch-meta">${g.members.length} member${g.members.length===1?'':'s'}</div>
          <div class="ch-actions"><button class="ch-action ${joined?'liked':''}" onclick="CH.toggleGroupJoin('${g.id}')">${joined?'✓ Joined':'+ Join group'}</button></div>
        </div>`;
      }).join('');
    }
  }

  /* ---------------- CHALLENGES ---------------- */
  function joinChallenge(id){
    const c = data.challenges.find(x=>x.id===id);
    if(!c.participants[me()]) c.participants[me()] = {checkins:[]};
    save(); renderChallenges();
  }

  function checkIn(id){
    const c = data.challenges.find(x=>x.id===id);
    const p = c.participants[me()]; if(!p) return;
    if(!p.checkins.includes(todayDate())) p.checkins.push(todayDate());
    save(); renderChallenges(); renderLeaderboard();
  }

  function renderChallenges(){
    const el = document.getElementById('chChallengesGrid');
    if(el) {
      el.innerHTML = data.challenges.map(c=>{
        const joined = !!c.participants[me()];
        const streak = joined ? c.participants[me()].checkins.length : 0;
        const doneToday = joined && c.participants[me()].checkins.includes(todayDate());
        const total = Object.keys(c.participants).length;
        return `<div class="ch-card">
          <div class="ch-username">${esc(c.name)}</div>
          <p style="font-size:13px;color:var(--text-secondary);margin:8px 0;">${esc(c.desc)}</p>
          <div class="ch-meta">${total} participant${total===1?'':'s'}${joined?' · your streak: '+streak+' day(s)':''}</div>
          <div class="ch-actions">
            ${!joined?`<button class="ch-action" onclick="CH.joinChallenge('${c.id}')">+ Join challenge</button>`
              :`<button class="ch-action ${doneToday?'liked':''}" onclick="CH.checkIn('${c.id}')">${doneToday?'✓ Checked in today':'Check in today'}</button>`}
          </div>
        </div>`;
      }).join('');
    }
  }

  /* ---------------- LEADERBOARD ---------------- */
  function renderLeaderboard(){
    const likesByUser = {};
    data.posts.forEach(p=>{ likesByUser[p.userId] = (likesByUser[p.userId]||0) + p.likes.length; });
    const ranked = data.users.map(u=>({u, score: (likesByUser[u.id]||0) + (u.followers?u.followers.length:0)}))
      .sort((a,b)=>b.score-a.score).slice(0,10);
    const el = document.getElementById('chLeaderboardBox');
    if(el) {
      el.innerHTML = `
        <h4 style="font-family:'Outfit',sans-serif;text-transform:uppercase;font-size:16px;letter-spacing:0.05em;margin-bottom:12px;">Weekly Leaderboard</h4>
        ${ranked.map((r,i)=>`<div class="ch-lb-row"><span class="ch-lb-rank">#${i+1}</span><span style="flex:1;padding-left:10px;">${esc(r.u.name)}</span><span class="ch-meta">${r.score} pts</span></div>`).join('') || '<div class="ch-empty">No activity yet.</div>'}
      `;
    }
  }

  /* ---------------- MESSAGES ---------------- */
  let activeChatId = null;
  function convKey(a,b){ return [a,b].sort().join('__'); }

  function openChat(id){
    activeChatId = id;
    const msgTabBtn = document.querySelector('.ch-tab-btn[data-ch="messages"]');
    if(msgTabBtn) msgTabBtn.click();
    renderChatUsers(); renderChatMsgs();
  }

  function renderChatUsers(){
    const el = document.getElementById('chChatUsers');
    if(el) {
      const others = data.users.filter(u=>u.id!==me());
      el.innerHTML = others.map(u=>`<div class="ch-chat-user ${u.id===activeChatId?'active':''}" onclick="CH.openChat('${u.id}')">${esc(u.name)}</div>`).join('');
    }
  }

  function renderChatMsgs(){
    const box = document.getElementById('chChatMsgs');
    if(!box) return;
    if(!activeChatId){ box.innerHTML = '<div class="ch-empty">Select a member to start chatting.</div>'; return; }
    const key = convKey(me(), activeChatId);
    const msgs = data.messages[key] || [];
    box.innerHTML = msgs.map(m=>`<div class="ch-msg ${m.from===me()?'me':'them'}">${esc(m.text)}</div>`).join('') || '<div class="ch-empty">No messages yet — say hello.</div>';
    box.scrollTop = box.scrollHeight;
  }

  function sendMessage(){
    if(!activeChatId){ alert('Pick a member to message first.'); return; }
    const input = document.getElementById('chMsgText');
    const text = input.value.trim(); if(!text) return;
    const key = convKey(me(), activeChatId);
    data.messages[key] = data.messages[key] || [];
    data.messages[key].push({from:me(), to:activeChatId, text, date:todayDate()});
    input.value=''; save(); renderChatMsgs();
  }

  /* ---------------- PROFILE ---------------- */
  function renderProfile(){
    const u = userById(me()); if(!u) return;
    const myPosts = data.posts.filter(p=>p.userId===u.id);
    const saved = (u.bookmarks||[]).map(id=>data.posts.find(p=>p.id===id)).filter(Boolean);
    const el = document.getElementById('chProfileBox');
    if(el) {
      el.innerHTML = `
        <div class="ch-user-row"><div class="ch-avatar" style="width:64px;height:64px;font-size:22px;">${esc(u.name).charAt(0)}</div>
          <div><div class="ch-username" style="font-size:18px;">${esc(u.name)}</div><div class="ch-meta">${esc(u.city||'')} · ${u.experience||'beginner'}</div></div></div>
        <div class="field-grid" style="margin-top:16px;">
          <div class="field"><label>Bio</label><textarea id="chBio">${esc(u.bio||'')}</textarea></div>
          <div class="field"><label>Height (cm)</label><input type="number" id="chHeight" value="${esc(u.height||'')}"></div>
          <div class="field"><label>Weight (kg)</label><input type="number" id="chWeight" value="${esc(u.weight||'')}"></div>
        </div>
        <div class="form-nav"><span></span><button class="btn small" type="button" onclick="CH.saveProfile()">Save profile</button></div>
        <div class="stat-row" style="margin-top:20px;">
          <div class="stat"><div class="label">Posts</div><div class="num" style="font-size:20px;">${myPosts.length}</div></div>
          <div class="stat"><div class="label">Followers</div><div class="num" style="font-size:20px;">${(u.followers||[]).length}</div></div>
          <div class="stat"><div class="label">Following</div><div class="num" style="font-size:20px;">${(u.following||[]).length}</div></div>
          <div class="stat"><div class="label">Badges</div><div class="num" style="font-size:20px;">${badgesFor(u).length}</div></div>
        </div>
        <div style="margin-top:14px;">${badgesFor(u).map(b=>`<span class="ch-badge">${esc(b)}</span>`).join('')}</div>
        <h4 style="font-family:'Outfit',sans-serif;text-transform:uppercase;font-size:14px;letter-spacing:0.05em;margin:22px 0 10px;">Your gallery</h4>
        <div class="ch-grid">${myPosts.length ? myPosts.map(postCard).join('') : '<div class="ch-empty">No posts yet.</div>'}</div>
        <h4 style="font-family:'Outfit',sans-serif;text-transform:uppercase;font-size:14px;letter-spacing:0.05em;margin:22px 0 10px;">Saved posts</h4>
        <div class="ch-grid">${saved.length ? saved.map(postCard).join('') : '<div class="ch-empty">Nothing saved yet.</div>'}</div>
      `;
    }
  }

  function saveProfile(){
    const u = userById(me());
    u.bio = document.getElementById('chBio').value;
    u.height = document.getElementById('chHeight').value;
    u.weight = document.getElementById('chWeight').value;
    save(); renderProfile();
  }

  // Self-boot initializer
  document.addEventListener('DOMContentLoaded', () => {
    boot();
  });

  return {
    join, createPost, toggleLike, toggleComments, addComment, share, toggleSave,
    askQuestion, replyQuestion, toggleFollow, renderPartners, createGroup, toggleGroupJoin,
    joinChallenge, checkIn, openChat, sendMessage, saveProfile
  };
})();
window.CH = CH; // Make available globally
