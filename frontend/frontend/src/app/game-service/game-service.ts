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
   hit(): Observable<GameState>{
    // TODO get game id
    return (this.http.post<GameState>(`${this.baseUrl}/games/0/hit`, {}))
  }

  async startNewGame(): Promise<Observable<GameState>>{
    const result = await firstValueFrom(
      this.http.post<GameState>(`${this.baseUrl}/games`, {})
    );
    // TODO use game id
    return this.http.post<GameState>(`${this.baseUrl}/games/0/deal`, {})
  }

  stand(): Observable<GameState>{
    // TODO get game id
    return (this.http.post<GameState>(`${this.baseUrl}/games/0/stand`, {}))
  }

  reset(): Observable<GameState>{
    // TODO get game id
    return (this.http.post<GameState>(`${this.baseUrl}/games/0/reset`, {}))
  }

}

// TODO replace strings with specific types
export type GameState = {
  hand : string[],
  dealer_hand : string[],
  dealer_value : number,
  value : number,
  game_state : string,
  winner : string
}
