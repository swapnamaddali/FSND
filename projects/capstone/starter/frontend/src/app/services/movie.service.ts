import { Injectable } from '@angular/core';
import { Observable, of, throwError } from 'rxjs';
import { HttpClient, HttpHeaders, HttpErrorResponse } from '@angular/common/http';
import { retry, catchError, tap, map } from 'rxjs/operators';
import { Movie } from '../classes/movie';
import { Actor } from '../classes/actor';
import { AuthService } from '../services/auth.service';
import { Router } from "@angular/router";
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class MovieService {

    apiURL = environment.apiServerUrl;
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
        const url = `${this.apiURL}/movies`;
        return this.http.get<Movie[]>(url);
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
        const url = `${this.apiURL}/movies/${id}`;
        return this.http.get<Movie>(url,
            this.getHeaders()).pipe(catchError(this.handleError)
            );
    }

    updateMovie(id, movie) {
        const url = `${this.apiURL}/movies/${id}`;
        this.http.patch(url, movie, this.getHeaders())
            .subscribe( (res: any) => {
                if (res.success) {
                    this.router.navigateByUrl('/movies');
                }
        });
    }

    deleteMovie(id) :Observable<{}> {
        const url = `${this.apiURL}/movies/${id}`;
        return this.http.delete(url, this.getHeaders())
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
        const url = `${this.apiURL}/actmovs/${id}`;
        this.http.patch(url, this.model, this.getHeaders())
            .subscribe( (res: any) => {
                if (res.success) {
                    console.log("updated");
                }
        });
    }

    deleteActMovie(id) :Observable<{}> {
        const url = `${this.apiURL}/actmovs/${id}`;
        return this.http.delete(url, this.getHeaders())
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
