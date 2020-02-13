import { Injectable } from '@angular/core';
import { Observable, of, throwError } from 'rxjs';
import { HttpClient, HttpHeaders, HttpErrorResponse } from '@angular/common/http';
import { retry, catchError, tap, map } from 'rxjs/operators';
import { Movie } from '../classes/movie';
import { Actor } from '../classes/actor';
import { AuthService } from '../services/auth.service';
import { Router } from "@angular/router";

@Injectable({
  providedIn: 'root'
})
export class MovieService {

    apiURL = 'http://127.0.0.1:5000';
    model:any;

    constructor(private auth: AuthService,
        private router: Router,
        private http: HttpClient) { }

   getHeaders() {
     const header = {
       headers: new HttpHeaders()
         .set('Authorization',  `Bearer ${this.auth.activeJWT()}`)
     };
     return header;
   }

    public getMovies(): Observable<Movie[]> {
      return this.http.get<Movie[]>(`http://127.0.0.1:5000/movies`);
    }

    public addMovie(movie: Movie) {
        this.http.post(this.apiURL + '/movies', movie, this.getHeaders())
        .subscribe( (res: any) => {
          if (res.success) {
            this.router.navigateByUrl('/movies');
          }
        });
    }

    getMovie(id): Observable<Movie> {
        return this.http.get<Movie>(`http://127.0.0.1:5000/movies/${id}`,
            this.getHeaders()).pipe(catchError(this.handleError)
            );
    }

    updateMovie(id, movie) {
        this.http.patch(`http://127.0.0.1:5000/movies/${id}`, movie, this.getHeaders())
            .subscribe( (res: any) => {
                if (res.success) {
                    this.router.navigateByUrl('/movies');
                }
        });
    }

    deleteMovie(id) :Observable<{}> {
        return this.http.delete(`http://127.0.0.1:5000/movies/${id}`, this.getHeaders())
            .pipe(catchError(this.handleError)
            );
    }

    getActorsByMovie(movieid): Observable<Actor[]> {
      return this.http.get<Actor[]>(this.apiURL+'/movies/'+movieid+'/actors', this.getHeaders())
      .pipe(catchError(this.handleError)
      );
    }

    updateActMv(id, sdate, edate) {
         this.model = {
          start_date: sdate,
          end_date: edate
        };
        this.http.patch(`http://127.0.0.1:5000/actmovs/${id}`, this.model, this.getHeaders())
            .subscribe( (res: any) => {
                if (res.success) {
                    console.log("updated");
                }
        });
    }

    deleteActMovie(id) :Observable<{}> {
        return this.http.delete(`http://127.0.0.1:5000/actmovs/${id}`, this.getHeaders())
            .pipe(catchError(this.handleError)
            );
    }

    // Error handling
    private handleError(error: HttpErrorResponse) {
          if (error.error instanceof ErrorEvent) {
            // A client-side or network error occurred. Handle it accordingly.
            console.error('An error occurred:', error.error.message);
          } else {
            // The backend returned an unsuccessful response code.
            // The response body may contain clues as to what went wrong,
            console.error(
              `Backend returned code ${error.status}, ` +
              `body was: ${error.error}`);
          }
          // return an observable with a user-facing error message
          return throwError(
            'Something bad happened; please try again later.');
    };
}
