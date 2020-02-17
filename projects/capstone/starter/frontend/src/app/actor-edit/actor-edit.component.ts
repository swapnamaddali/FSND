import { Component, OnInit } from '@angular/core';
import { ActorService } from '../services/actor.service';
import { Actor } from '../classes/actor';
import { Router, ActivatedRoute } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-actor-edit',
  templateUrl: './actor-edit.component.html',
  styleUrls: ['./actor-edit.component.css']
})
export class ActorEditComponent implements OnInit {

    model: Actor;
    _id:number;
    loading=true;
    gedvals = ['Male', 'Female'];
    submitted = false;

  constructor(private router: Router,
        private route: ActivatedRoute,
        public aService: ActorService) { }

  ngOnInit() {
      this.getActor(this.route.snapshot.params['id']);
  }

  getActor(id) {
      this.aService.getActor(id).subscribe( act => {
          this.loadData(act);
          this.loading = false;
      },(err) => {
          console.log(err);
      });
  }

  public loadData(act):void{
      this._id = act.actor.id;
      this.model = act.actor;
  }

  updateActor() {
      this.submitted = true;
      this.aService.updateActor(this._id, this.model);
  }

}
