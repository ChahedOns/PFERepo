import{ Component, OnInit, AfterViewInit } from '@angular/core';

import * as L from 'leaflet'


import "leaflet/dist/images/marker-shadow.png";
import "leaflet/dist/images/marker-icon.png";
import "leaflet/dist/images/marker-icon-2x.png";
@Component({
  selector: 'app-map',
  templateUrl: './map.page.html',
  styleUrls: ['./map.page.scss'],
})
export class MapPage implements  OnInit ,AfterViewInit {
  map : L.Map
  smallIcon = new L.Icon({
    iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-icon.png',
    iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-icon-2x.png',
    iconSize:    [25, 41],
    iconAnchor:  [12, 41],
    popupAnchor: [1, -34],
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    shadowSize:  [41, 41]
  });

  places : [{lat : 75.2369 , lng : 2.547859} , {lat : 74.2369 , lng : 3.547859} , {lat : 65.2369 , lng : 2.547859}]
  constructor() {}
  ngOnInit () {

  }
  ngAfterViewInit(): void {
    this.createMap();
    setTimeout(() => {
      this.map.invalidateSize();
    }, 400);
  }

  createMap() {

    const center= {
      lat: 46.227638,
      lng: 2.213749,
    };

    const zoomLevel = 12;

    this.map = L.map('map', {
      center: [center.lat, center.lng],
      zoom: zoomLevel
    });

    const mainLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      minZoom: 0,
      maxZoom: 50,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    });


      mainLayer.addTo(this.map);
      const descriptionWikipedia = `okeeey`;
      const popupOptions = {
        coords: center,
        text: descriptionWikipedia,
        open: true
      };
        this.addMarker(popupOptions);


  }

  addMarker({coords, text, open}) {
    const marker = L.marker([coords.lat, coords.lng], { icon: this.smallIcon });
    if (open) {
      marker.addTo(this.map).bindPopup(text).openPopup();
    } else {
      marker.addTo(this.map).bindPopup(text);
    }
  }
}


