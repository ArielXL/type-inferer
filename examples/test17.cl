class A {};
class B inherits A {};
class C inherits A {};
class D inherits B {};
class E inherits B {};
class F inherits C {};

class T inherits IO {};

class Main inherits IO {

	a: AUTO_TYPE;
	b: AUTO_TYPE;
	c: AUTO_TYPE;
	d: AUTO_TYPE;

	main() : AUTO_TYPE {
		{
			not a;
			~ b;
			while d loop 3 pool;
			if c then 1 else 2 fi;
		}
	};
	m(x: AUTO_TYPE, y: AUTO_TYPE, z: AUTO_TYPE, r: AUTO_TYPE) : AUTO_TYPE {
		{
			not x;
			~ y;
			while z loop 3 pool;
			if r then 1 else 2 fi;
		}
	};
};