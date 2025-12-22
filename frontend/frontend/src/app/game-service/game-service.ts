import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable, firstValueFrom} from 'rxjs';
import {environment} from '../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class GameService {
  private baseUrl = environment.apiUrl;

  constructor(private http:HttpClient){}

  // TODO implement security / nonce woth backend
   hit(id:number): Observable<GameState>{
    return (this.http.post<GameState>(`${this.baseUrl}/games/${id}/hit`, {}))
  }

  async startNewGame(): Promise<Observable<GameState>>{
    const result = await firstValueFrom(
      this.http.post<GameState>(`${this.baseUrl}/games`, {})
    );
    return this.deal(result.id)
  }

  deal(id:number):Observable<GameState>{
    return this.http.post<GameState>(`${this.baseUrl}/games/${id}/deal`, {})
  }

  stand(id:number): Observable<GameState>{
    return (this.http.post<GameState>(`${this.baseUrl}/games/${id}/stand`, {}))
  }

  reset(id:number): Observable<GameState>{
    return (this.http.post<GameState>(`${this.baseUrl}/games/${id}/reset`, {}))
  }

}

// TODO replace strings with specific types
export type GameState = {
  id : number,
  hand : string[],
  dealer_hand : string[],
  dealer_value : number,
  value : number,
  game_state : string,
  winner : string
}
