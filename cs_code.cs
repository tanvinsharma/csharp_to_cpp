public bool do_work(string param1, double param2, YetAnotherClass param3){

	SomeClass obj = new SomeClass(param1, param2);
	double number = 10.5;
	try{
		double result = obj.do_action(number);
		if(result >= 7 && result % 2 == 0 || number == 12){
			List<string> vec = new List<string>();
			vec.Add("this");
			vec.Add("is");
			vec.Add("an");
			vec.Add("example");
			foreach(var elem in vec){
				Console.WriteLine(elem);
			}
		}
	}
	catch(Exception e){
		Console.WriteLine(e.Message);
	}
}