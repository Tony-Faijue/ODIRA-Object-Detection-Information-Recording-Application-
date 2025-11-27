import { Component, signal, Signal } from '@angular/core';
import { FormsModule, NgModel} from '@angular/forms'
@Component({
  selector: 'app-settings',
  imports: [FormsModule],
  templateUrl: './settings.html',
  styleUrl: './settings.css',
})
export class Settings {

  categories = [
    { id: '1', name:"vehicles" , checked: false, label:"Vehicles"},
    { id: '2', name:"people" , checked: false, label:"People"},
    { id: 'clothes', name:"clothes" , checked: false, label:"Clothes & Accessories"},
    { id: 'animals', name:"animals" , checked: false, label:"Animals"},   
    { id: 'furniture', name:"furniture" , checked: false, label:"Furniture"},
    { id: 'food', name:"food" , checked: false, label:"Food"},
    { id: 'kitchen', name:"kitchen" , checked: false, label:"Kitchen"},
    { id: 'sports', name:"sports" , checked: false, label:"Sports"},
    { id: 'street', name:"street" , checked: false, label:"Street Items"},
    { id: 'electronics', name:"electronics" , checked: false, label:"Electronics"},
    { id: 'misc', name:"misc" , checked: false, label:"Miscellaneous"},
  ];

  selectAllChecked:boolean = false;
  objThresh:Signal<number> = signal(0.5);
  nmsThresh:Signal<number> = signal(0.2);


  /**
   * Method for toggling the select all check box
   */
  public toggleAll(){
    this.categories.forEach(category => category.checked = this.selectAllChecked);
  }
  /**
   * Method to update the select all check box when all items are selected or not 
   */
  public updateSelectAllChecked(){
    let allChecked = this.categories.every(category => category.checked);
    if(allChecked == true){
      this.selectAllChecked = true;
    } else {
      this.selectAllChecked = false;
    }
  }




}
