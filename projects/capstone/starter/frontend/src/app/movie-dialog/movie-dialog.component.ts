import { Component, OnInit, Inject } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { MAT_DIALOG_DATA } from '@angular/material';
import { Actor } from '../classes/actor';
import { MovieService } from '../services/movie.service';
import { DatePipe } from '@angular/common';

@Component({
  selector: 'app-movie-dialog',
  templateUrl: './movie-dialog.component.html',
  styleUrls: ['./movie-dialog.component.css']
})
export class MovieDialogComponent implements OnInit {

  modalTitle: string;
  objId:number;
  loading=true;
  acts_in_movie: any[];
  stDate: String;
  endDate: String;
  edit: boolean = false;

  constructor(@Inject(MAT_DIALOG_DATA) public data: any,
                public dialogRef: MatDialogRef<MovieDialogComponent>,
                public mvService: MovieService,
                private datePipe: DatePipe) {
    this.modalTitle = data.title;
    this.objId = data.id;
  }

  ngOnInit() {
      this.mvService.getActorsByMovie(this.objId)
      .subscribe( acts => {
          this.loadActorsByMovie(acts);
          this.loading = false;
      },(err) => {
          console.log(err);
      });
  }

  public loadActorsByMovie(acts):void {
    this.acts_in_movie = acts.actors;
    this.acts_in_movie.forEach((item) => {
        //item.sdate = this.datePipe.transform(item.sdate,"MM-dd-yyyy");
        item.sdate = new Date(item.sdate);
        //item.edate = this.datePipe.transform(item.edate,"MM-dd-yyyy");
        item.edate = new Date(item.edate);
    })
  }

  public reloadData(id):void {
      this.acts_in_movie = this.acts_in_movie.filter(movie => movie.actmovid !== id);
  }

  closeModal() {
    this.dialogRef.close();
  }

  saveActMov(act){
      this.mvService.updateActMv(act.id, act.sdate, act.sdate);
      this.edit = false;

  }

  deleteactmov(id){
      this.mvService.deleteActMovie(id)
      .subscribe( mvs => {
          this.reloadData(id)
      },(err) => {
          console.log(err);
      });
  }

}
