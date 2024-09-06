import { reverse_map } from "./utils.js";

export const fdc_ids = {
    1750339: 'Apple',
    169236: 'Artichoke',
    171705: 'Avocado',
    1103307: 'BBQ sauce',
    749420: 'Bacon',
    167533: 'Bagel',
    1105314: 'Banana',
    746763: 'Beef',
    1104393: 'Beer',
    171711: 'Blueberries',
    325871: 'Bread',
    747447: 'Broccoli',
    790508: 'Butter',
    169975: 'Cabbage',
    167990: 'Candy',
    746770: 'Cantaloupe',
    746764: 'Carrot',
    328637: 'Cheese',
    171719: 'Cherry',
    173630: 'Chicken wings',
    1104406: 'Cocktail',
    170169: 'Coconut',
    1104137: 'Coffee',
    333008: 'Cookie',
    167537: 'Corn chips',
    170857: 'Cream',
    168409: 'Cucumber',
    172756: 'Doughnut',
    1101515: 'Dumpling',
    171287: 'Egg',
    111111: 'Egg tart',
    169228: 'Eggplant',
    333374: 'Fish',
    170698: 'French fries',
    111112: 'Fries',
    1104647: 'Garlic',
    173040: 'Grape',
    174673: 'Grapefruit',
    321611: 'Green beans',
    170006: 'Green onion',
    1102734: 'Guacamole',
    170693: 'Hamburger',
    111113: 'Hamimelon',
    169640: 'Honey',
    167575: 'Ice cream',
    1102667: 'Kiwi fruit',
    167746: 'Lemon',
    746769: 'Lettuce',
    168155: 'Lime',
    174208: 'Lobster',
    169910: 'Mango',
    171638: 'Meat ball',
    746782: 'Milk',
    172765: 'Muffin',
    1999629: 'Mushroom',
    168914: 'Noodles',
    323294: 'Nuts',
    169260: 'Okra',
    748608: 'Olive oil',
    169095: 'Olives',
    1104962: 'Onion',
    746771: 'Orange',
    2003597: 'Orange juice',
    175009: 'Pancake',
    169926: 'Papaya',
    168927: 'Pasta',
    1104913: 'Pastry',
    325430: 'Peach',
    746773: 'Pear',
    170108: 'Pepper',
    175020: 'Pie',
    169124: 'Pineapple',
    173292: 'Pizza',
    169949: 'Plum',
    169134: 'Pomegranate',
    167959: 'Popcorn',
    170026: 'Potato',
    1099155: 'Prawns',
    169064: 'Pretzel',
    168448: 'Pumpkin',
    169276: 'Radish',
    169977: 'Red cabbage',
    168930: 'Rice',
    1103408: 'Salad',
    746775: 'Salt',
    1103330: 'Sandwich',
    746779: 'Sausages',
    174852: 'Soft drink',
    1999632: 'Spinach',
    1102056: 'Spring rolls',
    746762: 'Steak',
    747448: 'Strawberries',
    1102350: 'Sushi',
    174144: 'Tea',
    1999634: 'Tomato',
    170054: 'Tomato sauce',
    175038: 'Waffle',
    167765: 'Watermelon',
    174837: 'Wine',
    169291: 'Zucchini',
};

export const fdc_ids_as_array = Object.values(fdc_ids).sort();

// Setup fdc_ids reversed mapped with food names as index
export const fdc_ids_string_index = reverse_map(fdc_ids);