import { Component, OnInit, Inject } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { MAT_DIALOG_DATA } from '@angular/material';
import { Movie } from '../classes/movie';
import { ActorService } from '../services/actor.service';

@Component({
  selector: 'app-actor-dialog',
  templateUrl: './actor-dialog.component.html',
  styleUrls: ['./actor-dialog.component.css']
})
export class ActorDialogComponent implements OnInit {

    modalTitle: string;
    objId:number;
    loading=true;
    moviesList: Movie[];

    constructor(@Inject(MAT_DIALOG_DATA) public data: any,
                  public dialogRef: MatDialogRef<ActorDialogComponent>,
                  public aService: ActorService) {
      this.modalTitle = data.title;
      this.objId = data.id;
    }

    ngOnInit() {
        this.aService.getActorMovies(this.objId)
        .subscribe( mvs => {
            this.loadMoviesByActor(mvs);
            this.loading = false;
        },(err) => {
            console.log(err);
        });
    }

    public loadMoviesByActor(mvs):void {
      this.moviesList = mvs.movies;
    }

    // If the user clicks the cancel button a.k.a. the go back button, then\
    // just close the modal
    closeModal() {
      this.dialogRef.close();
    }

}
