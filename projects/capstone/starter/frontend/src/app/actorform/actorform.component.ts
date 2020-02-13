import { Component, OnInit } from '@angular/core';
import { ActorService } from '../services/actor.service';
import { Actor } from '../classes/actor';


@Component({
  selector: 'app-actorform',
  templateUrl: './actorform.component.html',
  styleUrls: ['./actorform.component.css']
})
export class ActorformComponent implements OnInit {

    model = new Actor();

    gedvals = ['Male', 'Female'];

    constructor(public aService: ActorService) { }

    ngOnInit() { }

    public addActor(){
        this.aService.addActor(this.model);
    }

}
