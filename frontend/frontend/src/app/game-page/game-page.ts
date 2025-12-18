import { Component, ChangeDetectorRef   } from '@angular/core';
import {GameService} from '../game-service/game-service'
import {GameState} from '../game-service/game-service';
import {NgIf} from '@angular/common'

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

  // TODO show game status, dealt, game id, etc
  updateStatus(data: GameState){
    this.gameState = data;

    // forces DOM to update to show new status
    this.cdr.detectChanges();
  }

  hit(){
    this.gameService.hit().subscribe((data:GameState) =>{
      this.updateStatus(data);
    });
  }

  stand(){
    this.gameService.stand().subscribe((data:GameState) =>{
      this.updateStatus(data);
    });
  }

  reset(){
    this.gameService.reset().subscribe((data:GameState) =>{
      this.updateStatus(data);
    });

  }

  // is async because we await new game to be made, then deal
  // could probably handle a bit better
  async newGame(){
    (await this.gameService.startNewGame()).subscribe((data:GameState) =>{
      this.updateStatus(data);
    });
  }
}
