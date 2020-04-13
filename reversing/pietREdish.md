Piet RE dish...oh man...where to start with this.

I wrote this challenge inspired by a piet challenge at [UMDCTF](https://umdctf.io/) in 2019.

I'm going to start off by saying this challenge wasn't the kindest, which is why it was worth so many points.
That said, it's certainly solvable with no prior experience. 

If you google `piet coding` or `piet language`, the esoteric language comes up almost right away.

You can see from any example that this code is executional, and seems to simply execute assembly (sorta) embedded in an image.

From there, by looking at the piet code in pietREdish, you can see that it looks like there's a block that executes, then a HUGE branch.

Branches typically indicate something must be satisfied, and if you look at the line before the branch, you might see what looks like some sort of repeating encoding.
You can do some physical analysis in paint with the [piet docs](https://www.dangermouse.net/esoteric/piet.html) to figure out that it's setting a value to 0, and from there, it branches or doesn't.
If you'd like to see something branch differently than on a 0, I'd typically recommend changing that 0 to not a 0 by changing a single pixel.

After changing a single pixel, that long branch executes, and the flag is printed instead of nothing.

-----------------------------------------------

Other solutions include changing random pixels to red until it does what you want it to do (cited by anonymous during the competition).

The solve picture shows the code recompiled (though this changes more than the simple thing needed).
