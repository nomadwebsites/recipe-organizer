#!/usr/bin/env python3
"""
Sample data seeder for Recipe Organizer
Run this to populate your database with example recipes for testing
"""

import database

def seed_sample_recipes():
    """Add sample recipes to the database"""
    
    print("Seeding sample recipes...")
    
    # Recipe 1: Spaghetti Carbonara
    database.create_recipe(
        name="Spaghetti Carbonara",
        description="Classic Italian pasta dish with eggs, cheese, and pancetta",
        ingredients=[
            "400g spaghetti",
            "200g pancetta or guanciale, diced",
            "4 large eggs",
            "100g Pecorino Romano cheese, grated",
            "Black pepper to taste",
            "Salt for pasta water"
        ],
        instructions=[
            "Bring a large pot of salted water to boil",
            "Cook spaghetti according to package directions until al dente",
            "While pasta cooks, fry pancetta in a large pan until crispy",
            "In a bowl, whisk together eggs, cheese, and black pepper",
            "Drain pasta, reserving 1 cup pasta water",
            "Add hot pasta to the pan with pancetta",
            "Remove from heat and quickly stir in egg mixture",
            "Add pasta water as needed to create a creamy sauce",
            "Serve immediately with extra cheese and black pepper"
        ],
        prep_time="10 minutes",
        cook_time="15 minutes",
        servings="4 servings",
        tags=["Italian", "Pasta", "Dinner", "Quick"]
    )
    
    # Recipe 2: Chocolate Chip Cookies
    database.create_recipe(
        name="Classic Chocolate Chip Cookies",
        description="Crispy on the outside, chewy on the inside chocolate chip cookies",
        ingredients=[
            "2 1/4 cups all-purpose flour",
            "1 tsp baking soda",
            "1 tsp salt",
            "1 cup butter, softened",
            "3/4 cup granulated sugar",
            "3/4 cup packed brown sugar",
            "2 large eggs",
            "2 tsp vanilla extract",
            "2 cups chocolate chips"
        ],
        instructions=[
            "Preheat oven to 375°F (190°C)",
            "Mix flour, baking soda, and salt in a bowl",
            "In another bowl, beat butter and sugars until creamy",
            "Add eggs and vanilla to butter mixture and beat well",
            "Gradually blend in flour mixture",
            "Stir in chocolate chips",
            "Drop rounded tablespoons of dough onto ungreased cookie sheets",
            "Bake for 9-11 minutes or until golden brown",
            "Cool on baking sheet for 2 minutes",
            "Transfer to wire rack to cool completely"
        ],
        prep_time="15 minutes",
        cook_time="10 minutes",
        servings="48 cookies",
        tags=["Dessert", "Baking", "Cookies", "Sweet"]
    )
    
    # Recipe 3: Greek Salad
    database.create_recipe(
        name="Traditional Greek Salad",
        description="Fresh and healthy Mediterranean salad with feta cheese",
        ingredients=[
            "4 large tomatoes, cut into wedges",
            "1 cucumber, sliced",
            "1 red onion, thinly sliced",
            "1 green bell pepper, cut into rings",
            "200g feta cheese, cubed",
            "1/2 cup Kalamata olives",
            "1/4 cup extra virgin olive oil",
            "2 tbsp red wine vinegar",
            "1 tsp dried oregano",
            "Salt and pepper to taste"
        ],
        instructions=[
            "Cut tomatoes into wedges and place in a large bowl",
            "Add sliced cucumber, onion, and bell pepper",
            "Add olives and feta cheese",
            "In a small bowl, whisk together olive oil, vinegar, oregano, salt, and pepper",
            "Pour dressing over salad",
            "Toss gently to combine",
            "Let sit for 10 minutes before serving to allow flavors to meld",
            "Serve at room temperature"
        ],
        prep_time="15 minutes",
        cook_time="0 minutes",
        servings="4 servings",
        tags=["Salad", "Healthy", "Vegetarian", "Mediterranean", "No-Cook"]
    )
    
    # Recipe 4: Chicken Stir-Fry
    database.create_recipe(
        name="Quick Chicken Stir-Fry",
        description="Fast and flavorful Asian-inspired chicken and vegetable stir-fry",
        ingredients=[
            "500g chicken breast, cut into strips",
            "2 tbsp vegetable oil",
            "1 red bell pepper, sliced",
            "1 yellow bell pepper, sliced",
            "200g broccoli florets",
            "2 cloves garlic, minced",
            "1 tbsp fresh ginger, grated",
            "3 tbsp soy sauce",
            "2 tbsp oyster sauce",
            "1 tbsp sesame oil",
            "1 tsp cornstarch",
            "Green onions for garnish"
        ],
        instructions=[
            "Mix soy sauce, oyster sauce, sesame oil, and cornstarch in a small bowl",
            "Heat vegetable oil in a large wok or skillet over high heat",
            "Add chicken and stir-fry for 5-6 minutes until cooked through",
            "Remove chicken and set aside",
            "Add more oil if needed, then add garlic and ginger",
            "Stir-fry for 30 seconds until fragrant",
            "Add bell peppers and broccoli, stir-fry for 3-4 minutes",
            "Return chicken to the wok",
            "Pour sauce over everything and toss to coat",
            "Cook for 1-2 minutes until sauce thickens",
            "Garnish with green onions and serve with rice"
        ],
        prep_time="15 minutes",
        cook_time="12 minutes",
        servings="4 servings",
        tags=["Asian", "Chicken", "Dinner", "Quick", "Healthy"]
    )
    
    # Recipe 5: Banana Bread
    database.create_recipe(
        name="Moist Banana Bread",
        description="Sweet and moist banana bread perfect for breakfast or snack",
        ingredients=[
            "3 ripe bananas, mashed",
            "2 cups all-purpose flour",
            "1 tsp baking soda",
            "1/4 tsp salt",
            "1/2 cup butter, melted",
            "3/4 cup brown sugar",
            "2 eggs, beaten",
            "1 tsp vanilla extract",
            "1/2 cup chopped walnuts (optional)"
        ],
        instructions=[
            "Preheat oven to 350°F (175°C)",
            "Grease a 9x5 inch loaf pan",
            "In a bowl, mix flour, baking soda, and salt",
            "In another bowl, mix melted butter and brown sugar",
            "Add eggs and vanilla to butter mixture",
            "Fold in mashed bananas",
            "Gently fold in flour mixture until just combined",
            "Stir in walnuts if using",
            "Pour batter into prepared loaf pan",
            "Bake for 60-65 minutes until a toothpick comes out clean",
            "Cool in pan for 10 minutes, then turn out onto a wire rack"
        ],
        prep_time="15 minutes",
        cook_time="65 minutes",
        servings="1 loaf (8-10 slices)",
        tags=["Baking", "Breakfast", "Snack", "Sweet"]
    )
    
    print("✅ Successfully added 5 sample recipes!")
    print("\nRecipes added:")
    print("  1. Spaghetti Carbonara")
    print("  2. Classic Chocolate Chip Cookies")
    print("  3. Traditional Greek Salad")
    print("  4. Quick Chicken Stir-Fry")
    print("  5. Moist Banana Bread")
    print("\nYou can now test the search functionality with keywords like:")
    print("  - 'chicken'")
    print("  - 'chocolate'")
    print("  - 'quick'")
    print("  - 'healthy'")

if __name__ == "__main__":
    # Initialize database if needed
    database.init_db()
    
    # Seed sample data
    seed_sample_recipes()
