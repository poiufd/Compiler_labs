{-# OPTIONS -fno-warn-tabs #-} 
import Data.List
import Text.Read
import Data.Maybe

first_step n e p s = let 
	{ne =  concat . map fst . filter ((=="e") . snd) $ p;
	subset w1 w2 = all (\l-> l `elem` w2) w1;
	filter_ne l = l `union` (concat . map fst . filter (\(a,b)->subset b l) $ p);
	find_ne old new
		| old == new = new
		| otherwise = find_ne new (filter_ne new)
	} 
	in find_ne [] ne

second_step s ne p = let
	{tuples (a,b) = if b == "e" 
		then [] 
		else let 
			{numbers = map snd $ filter (\(a,b)-> a `elem` ne ) (zip b [0,1..]); 
		 	subs =   subsequences numbers; 
		 	pre_rules = map (foldl (\acc pos->take pos acc ++ '_' : drop (pos+1) acc)  b ) subs;
		 	pre_filtered = filter (not . null) . map (filter (/='_') ) $ pre_rules;
			}
			in map (\el-> (a,el)) pre_filtered;
	rules = concat . map tuples $ p;		
	}
	in	rules 

read_input arr res = let {number = readMaybe (arr!!0):: Maybe Int} 
	in if isJust number
		then read_input (drop (fromJust number + 1) arr) (res ++ [tail $ take (fromJust number + 1) arr])
		else res ++ [[last arr]]

write_output::[Char]->[Char]->[([Char],[Char])]->[Char] -> IO ()
write_output n e p s = do
	let p' = map (\(a,b)-> a ++ "->"++ b ++ "\n") p;
		output_line = "Нетерминалы\n" ++ (n++"\n") ++ "Терминалы\n" ++ (e++"\n")
								++ "Правила\n" ;
	writeFile "output.txt" output_line
	mapM_ (appendFile "output.txt") p'
	appendFile "output.txt" "Начальный символ грамматики\n"
	appendFile "output.txt" s

main = do
	contents <- readFile "input.txt"
	let arr =  lines $ contents;
		args = read_input arr [];
		n = concat $ args!!0; e = concat $ args!!1;
		p = map (\ar-> let [a,b] = words ar in (a,b)) (args!!2);
		s = concat . last $ args;
		ne = first_step n e p s;
		p' = second_step s ne p;
	if s `isInfixOf` ne 
		then do
			let p''= p'++ [("S'","S"),("S'","e")];
				s' = "S'";
				n' = n ++ s';
			print $ n'	
			print $ e
			print $ p''
			print $ s'
			write_output n' e p'' s'
		else do	
			print $ n
			print $ e
			print $ p'
			print $ s
			write_output n e p' s

