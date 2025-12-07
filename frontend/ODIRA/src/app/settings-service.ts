import { Injectable, signal, Signal } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

export interface Category{
  id: string;
  name: string;
  checked: boolean;
  label: string;
}

export interface SettingsData{
  objThresh: number;
  nmsThresh: number;
  categories: Category[];
}

@Injectable({
  providedIn: 'root',
})
export class SettingsService {

  private initialSettings: SettingsData = {
    objThresh: 0.5,
    nmsThresh: 0.2,
    categories: [
    { id: 'vehicles', name:"vehicles" , checked: false, label:"Vehicles"},
    { id: 'people', name:"people" , checked: false, label:"People"},
    { id: 'clothes', name:"clothes" , checked: false, label:"Clothes & Accessories"},
    { id: 'animals', name:"animals" , checked: false, label:"Animals"},   
    { id: 'furniture', name:"furniture" , checked: false, label:"Furniture"},
    { id: 'food', name:"food" , checked: false, label:"Food"},
    { id: 'kitchen', name:"kitchen" , checked: false, label:"Kitchen"},
    { id: 'sports', name:"sports" , checked: false, label:"Sports"},
    { id: 'street', name:"street" , checked: false, label:"Street Items"},
    { id: 'electronics', name:"electronics" , checked: false, label:"Electronics"},
    { id: 'misc', name:"misc" , checked: false, label:"Miscellaneous"},
    ]
  };

  private settingsSubject = new BehaviorSubject<SettingsData>(this.initialSettings);
  public currentSettings: Observable<SettingsData> = this.settingsSubject.asObservable();

  /**
   * 
   * @param newSettings 
   * Update settings when a change occurs
   */
  updateSettings(newSettings: SettingsData): void{
    this.settingsSubject.next(newSettings);
  }

  /**
   * 
   * @returns the current settings data
   */
  currentSettingsSnapshot(): SettingsData {
    return this.settingsSubject.value;
  }
}
