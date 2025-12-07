import { Routes } from '@angular/router';
import { Odira } from './odira/odira';
import { AboutPage } from './about-page/about-page';

export const routes: Routes = [
    {path: '', component: Odira, title: 'ODIRA'}, // default route
    {path: 'about', component:AboutPage, title:'About'},
];
