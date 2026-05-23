import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';

export interface Category{
  name: string;
  items: string[]
}

@Component({
  selector: 'app-about-page',
  imports: [RouterLink, CommonModule],
  templateUrl: './about-page.html',
  styleUrl: './about-page.css',
})
export class AboutPage {

  activeCategoryIndex: number = 0;

  // Categories data

  vehicles: Category = {
    name: 'Vehicles',
    items: ['Bicycle','Car', 'Motorcycle', 'Bus', 'Train', 'Truck','Boat', 'Airplane']
  }

  clothes: Category = {
    name: 'Accessories',
    items: ['Backpack', 'Handbag', 'Suitcase', 'Tie', 'Hat', 'Eye Glasses', 'Shoe', 'Umbrella']
  }

  animals: Category = {
    name: 'Animals',
    items: ['Bird', 'Cat', 'Dog', 'Horse', 'Sheep', 'Cow', 'Elephant', 'Bear', 'Zebra', 'Giraffe']
  }

  furniture: Category = {
    name: 'Furniture',
    items: ['Chair', 'Couch', 'Bed', 'Mirror', 'Dinning Table', 'Window', 'Desk', 'Potted Plant', 'Toilet', 'Door', 'Sink', 'Clock', 'Vase']
  }

  food: Category = {
    name: 'Food',
    items: ['Banana', 'Apple', 'Orange', 'Pizza', 'Sandwich','Broccoli', 'Carrot', 'Hot Dog', 'Donut', 'Cake']
  }

  kitchen: Category = {
    name: 'Kitchen',
    items: ['Bottle', 'Plate', 'Wine Glass', 'Cup', 'Fork', 'Knife', 'Spoon', 'Bowl', 'Microwave', 'Oven', 'Toaster', 'Refrigerator', 'Blender']
  }

  sportsItems: Category = {
    name: 'Sports Items',
    items: ['Sports Ball', 'Frisbee', 'Kite', 'Baseball Bat', 'Baseball Glove', 'Skateboard', 'Snowboard', 'Surfboard', 'Tennis Racket', 'Skis']
  }

  streetItems: Category = {
    name: 'Street Items',
    items: ['Traffic Light', 'Stop Sign', 'Parking Meter', 'Street Sign', 'Bench', 'Fire Hydrant']
  }

  electronics: Category = {
    name: 'Electronics',
    items: ['TV', 'Laptop', 'Cell Phone', 'Remote', 'Keyboard', 'Mouse']
  }

  miscellaneous: Category = {
    name: 'Miscellaneous',
    items: ['Hair Drier', 'Hair Brush', 'Toothbrush', 'Teddy Bear', 'Book', 'Scissors']
  }

  people: Category = {
    name: 'People',
    items: ['Person']
  }
  // array of all categories
  categories: Category[] = [this.vehicles, this.clothes, this.animals, this.furniture, this.food, this.kitchen, this.sportsItems, this.streetItems, this.electronics, this.miscellaneous, this.people];

  /**
   * Function to select a catergory and show the items in that category
   * @param index 
   */
  public selectCategory(index: number): void {
    this.activeCategoryIndex = index;
  }

}
