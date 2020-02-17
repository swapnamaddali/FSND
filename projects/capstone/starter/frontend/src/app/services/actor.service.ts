import { Injectable } from '@angular/core';
import { Observable, of, throwError } from 'rxjs';
import { HttpClient, HttpHeaders, HttpErrorResponse } from '@angular/common/http';
import { retry, catchError, tap, map } from 'rxjs/operators';
import { Actor } from '../classes/actor';
import { Movie } from '../classes/movie';
import { Actmov } from '../classes/actmov';
import { AuthService } from '../services/auth.service';
import { Router } from "@angular/router";
import { environment } from '../../environments/environment';

const httpOptions = {
  headers: new HttpHeaders({'Content-Type': 'application/json'})
};

@Injectable({
  providedIn: 'root',
})
export class ActorService {

apiURL = environment.apiServerUrl;

actor = new Actor();

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

  public getActors(): Observable<Actor[]> {
    const url = `${this.apiURL}/actors`;
    return this.http.get<Actor[]>(url)
  }

  public addActor(actor: Actor) {
      this.http.post(this.apiURL + '/actors', actor, this.getHeaders())
      .subscribe( (res: any) => {
        if (res.success) {
          this.router.navigateByUrl('/actors');
        }
      });
  }

  public addActmov(actmov: Actmov) {
      this.http.post(this.apiURL + '/actmov', actmov, this.getHeaders())
      .subscribe( (res: any) => {
        if (res.success) {
          this.router.navigateByUrl('/movies');
        }
      });
  }

    getActor(id): Observable<Actor> {
        const url = `${this.apiURL}/actordetail/${id}`;
        return this.http.get<Actor>(url,
            this.getHeaders()).pipe(
              tap(_ => console.log(`fetched Actor id=${id}`)),
              catchError(this.handleError)
            );
    }

    updateActor(id, actor) {
        const url = `${this.apiURL}/actors/${id}`;
        this.http.patch(url, actor, this.getHeaders())
            .subscribe( (res: any) => {
                if (res.success) {
                    this.router.navigateByUrl('/actors');
                }
        });
    }

    deleteActor(id) :Observable<{}> {
        const url = `${this.apiURL}/actors/${id}`;
        return this.http.delete(url, this.getHeaders())
            .pipe(catchError(this.handleError)
            );
    }

    public getActorMovies(act_id):Observable<Movie[]> {
        return this.http.get<Movie[]>(this.apiURL+'/actors/'+act_id+'/movies')
        .pipe(catchError(this.handleError)
        );
    }

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
