import { Component, OnInit } from '@angular/core';
import {Router} from "@angular/router";
import { MovieService } from '../services/movie.service';
import { Movie } from '../classes/movie';
import { Actor } from '../classes/actor';
import { AuthService } from '../services/auth.service';
import { MatDialog, MatDialogConfig } from '@angular/material/dialog';
import { MovieDialogComponent } from '../movie-dialog/movie-dialog.component';

@Component({
  selector: 'app-movies',
  templateUrl: './movies.component.html',
  styleUrls: ['./movies.component.css']
})
export class MoviesComponent implements OnInit {

    mvs: Movie[];
    error: string;
    loading=true;

    constructor(public mvService: MovieService,
                public router: Router,
                public auth: AuthService,
                public matDialog: MatDialog) { }

    ngOnInit() {
        this.mvService.getMovies()
            .subscribe( mvs => {
                this.loadData(mvs)
                this.loading = false;
            },(err) => {
        console.log(err);
        });
    }

    public loadData(mvs):void{
        this.mvs = mvs.movies;
    }

    public reloadData(id):void {
        this.mvs = this.mvs.filter(movie => movie.id !== id);
    }

    deleteMovie(id) {
        this.mvService.deleteMovie(id)
        .subscribe( mvs => {
            this.reloadData(id)
        },(err) => {
            this.error = "Error Occurred"
        });
    }

    openModal(id, title) {
        const dialogConfig = new MatDialogConfig();
        // The user can't close the dialog by clicking outside its body
        dialogConfig.disableClose = true;
        dialogConfig.id = "modal-component";

        dialogConfig.data = {
            id: id,
            title: title
        };
        const modalDialog = this.matDialog.open(MovieDialogComponent, dialogConfig);
    }
}
