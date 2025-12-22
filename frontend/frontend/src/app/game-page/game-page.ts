import { Component, ChangeDetectorRef} from '@angular/core';
import {GameService} from '../game-service/game-service';
import {GameState} from '../game-service/game-service';
import {NgIf} from '@angular/common';
import { switchMap } from 'rxjs/operators';

@Component({
  selector: 'app-game-page',
  imports: [NgIf],
  templateUrl: './game-page.html',
  styleUrl: './game-page.css',
})
export class GameComponent {
  gameState:GameState | null = null;

  constructor(
    private gameService:GameService,
    private cdr : ChangeDetectorRef
  ){}

  getGameId():number{
    if (this.gameState?.id == null){
      throw Error("gameComponent tried to get id that wasn't initialized")
    }
    return this.gameState.id
  }

  updateStatus(data: GameState){
    this.gameState = data;

    // forces DOM to update to show new status
    this.cdr.detectChanges();
  }

  hit(){
    this.gameService.hit(this.getGameId()).subscribe((data:GameState) =>{
      this.updateStatus(data);
    });
  }

  stand(){
    this.gameService.stand(this.getGameId()).subscribe((data:GameState) =>{
      this.updateStatus(data);
    });
  }

  // sends 1 request to reset, and another to deal
  // logic should likely be in gameService instead
  reset(){
    this.gameService.reset(this.getGameId()).pipe(
      switchMap(() => this.gameService.deal(this.getGameId()))
    ).subscribe((data:GameState) => {
      this.updateStatus(data);
    });
  }

  // is async because we await new game to be made, then deal
  // could probably handle a bit better
  async newGame(){
    // create new game if needed
    if (this.gameState == null){
      (await this.gameService.startNewGame()).subscribe((data:GameState) =>{
        this.updateStatus(data);
      });
    }
    else{
      this.reset()
    }
  }
}
