import { Component, OnInit } from '@angular/core';
import {Router} from "@angular/router";
import { ActorService } from '../services/actor.service';
import { Actor } from '../classes/actor';
import { AuthService } from '../services/auth.service';
import { MatDialog, MatDialogConfig } from '@angular/material/dialog';
import { ActorDialogComponent } from '../actor-dialog/actor-dialog.component';

@Component({
  selector: 'app-actor',
  templateUrl: './actor.component.html',
  styleUrls: ['./actor.component.css']
})
export class ActorComponent implements OnInit {

    acts: Actor[];

    constructor(public aService: ActorService,
              public router: Router,
            public auth: AuthService,
            public matDialog: MatDialog) { }

    ngOnInit() {
        this.aService.getActors()
            .subscribe( acts => {
                this.loadData(acts)
            },(err) => {
        console.log(err);
        });
    }
    public loadData(acts):void{
        this.acts = acts.actors;
    }

    public reloadData(id):void {
        this.acts = this.acts.filter(actor => actor.id !== id);
    }

    deleteActor(id) {
        this.aService.deleteActor(id)
        .subscribe( acts => {
            this.reloadData(id)
        },(err) => {
            console.log(err);
        });
    }

    openModal(id, lastname, firstname) {
        const dialogConfig = new MatDialogConfig();
        // The user can't close the dialog by clicking outside its body
        dialogConfig.disableClose = true;
        dialogConfig.id = "modal-component";

        dialogConfig.data = {
            id: id,
            title: lastname+" "+firstname
        };
        const modalDialog = this.matDialog.open(ActorDialogComponent, dialogConfig);
    }
 }
