import { Component, inject, OnInit, signal, computed, effect } from '@angular/core';
import { FormsModule, NgModel} from '@angular/forms';
import { Category, SettingsData, SettingsService } from '../settings-service';

@Component({
  selector: 'app-settings',
  imports: [FormsModule],
  templateUrl: './settings.html',
  styleUrl: './settings.css',
})

export class Settings implements OnInit{

  private readonly settingsService = inject(SettingsService);

  categories: Category[] = [];
  selectAllChecked:boolean = true;

  //Signals fo UI display
  objThresh = signal(0.5);
  nmsThresh = signal(0.2);

  //Use of computed signal for settings data
  //signal updates automatically when objthresh or nmsthresh changes
  settingsDataComputed = computed<Omit<SettingsData, 'categories'>>(() => {
    return {
      objThresh: this.objThresh(),
      nmsThresh: this.nmsThresh(),
    };
  });

  
  constructor(){

    effect(() => {
      const currentThresholds = this.settingsDataComputed();
      //When the thresholds changes, update the service with the latest settings data
      this.settingsService.updateSettings({...currentThresholds, categories:this.categories});
      console.log("Setting Service data auto updated");
    });

  }

  public ngOnInit(): void {
    //Initialize local state from service snapshot 
    const currentSettings = this.settingsService.currentSettingsSnapshot();

    this.objThresh.set(currentSettings.objThresh);
    this.nmsThresh.set(currentSettings.nmsThresh);
    //Set all categories checked by default
    this.categories = currentSettings.categories.map(category => ({
      ...category,
       checked: category.checked !== undefined ? category.checked: true
      }));
    //Update the select all check box state based on the categories
    this.selectAllChecked = this.categories.length > 0 && this.categories.every(category => category.checked);
  }

  /**
   * Method for toggling the select all check box
   */
  public toggleAll(){
    this.categories.forEach(category => category.checked = this.selectAllChecked);
    this.triggerCategoryUpdate()
  }
  /**
   * Method to update the select all check box when all items are selected or not 
   */
  public updateSelectAllChecked(){
    this.selectAllChecked = this.categories.length > 0 && this.categories.every(category => category.checked);
    this.triggerCategoryUpdate();
  }

  /**
   * Method to update categories is setting service
   */
  public triggerCategoryUpdate(): void{
    const currentThresholds = this.settingsDataComputed();
    let dataToSave: SettingsData = {
      ...currentThresholds,
      categories: this.categories
    };
    this.settingsService.updateSettings(dataToSave);
    console.log('GlobalSetting Service with latest categories');
  }

}
