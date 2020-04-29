#include <bits/stdc++.h>
#include <ext/pb_ds/assoc_container.hpp> // Common file
#include <ext/pb_ds/tree_policy.hpp> // Including tree_order_statistics_node_update
using namespace std;
using namespace __gnu_pbds;

double INF = 1e100;
double EPS = 1e-12;
typedef long long int ll;

typedef pair < int,int > PII;
typedef pair < ll,ll > PLL;

typedef tree<
int,
null_type,
less<int>,
rb_tree_tag,
tree_order_statistics_node_update>
ordered_set;

#define F first
#define S second


ostream& operator<<(ostream & os, PLL h){
	return os << "( " << h.F << ", " << h.S << " )" << endl;

}
PLL operator+ (PLL a, ll x)     {return {a.F + x, a.S + x} ;}
PLL operator- (PLL a, ll x)     {return {a.F - x, a.S - x} ;}
PLL operator* (PLL a, ll x)     {return {a.F * x, a.S * x} ;}
PLL operator+(PLL x, PLL y) { return {x.F + y.F,x.S + y.S} ;}
PLL operator-(PLL x,PLL y) { return {x.F - y.F, x.S - y.S} ;}
PLL operator*(PLL x,PLL y) { return {x.F * y.F , x.S * y.S} ;}
PLL operator%(PLL x,PLL y) { return {x.F % y.F, x.S % y.S} ;}


ll const MOD = 998244353;
ll const MX = 1e5 + 10;
ll factorial[MX] ;
ll inv[MX] ;

ll bigmod(ll a, ll b){
	if(!b) return 1;
	ll x  = bigmod(a,b/2);

	x = (x * x)%MOD;
	if(b&1)
		x = (x * a) %MOD;
	return x;
}
ll modinv(ll num){
	return bigmod(num,MOD-2);
}

int const N = sqrt(1e15) + 100;
vector < ll > primes;
bitset <90000000> mark;
map<ll, vector<PLL> > prime_factors;

void sieve()
{

	factorial[0] = 1;
	for(int i = 1; i < MX; i++)
		factorial[i] = (factorial[i-1]*i) % MOD;
    //marks.resize(n+10,0);

	for(ll i = 0; i < MX; i++) 
		inv[i] = modinv(factorial[i]);

	mark.reset();

	for(ll i = 2; i * i < N; i++){
		if(mark[i]) continue;
		for(ll j = i * i; j < N ; j += i){
			mark[j] = 1;
		}
	}
	for(int i = 2; i < N ; i++) 
		if(!mark[i]) primes.push_back(i);
}
vector<PLL> pd;
void factorization(ll n){
	
	pd.clear();
	for(auto x : primes){
		//if(n < x) break;
		if(n % x == 0){
			int cnt = 0;
			while(n % x == 0) cnt++, n /= x;
			pd.emplace_back(x,cnt);
		}
	}
	if(n != 1) pd.emplace_back(n,1);
	
}
vector<PLL> tmp;
void backtrack(int pos, ll num){
	if(pos == pd.size()) {
		prime_factors[num] = tmp;
		return ;
	}
	ll fact = num;
	for(int i = 0; i <= pd[pos].second; i++){
		tmp.emplace_back(pd[pos].first,i);
		backtrack(pos+1,fact);
		tmp.pop_back();
		fact *= pd[pos].first ;
	}
}


int main(){

	ios::sync_with_stdio(false); cin.tie(0);
	int t;
	sieve();

	//cout << t << endl;

	ll d;
	cin >> d;
	//cout << d << endl;
	prime_factors.clear();
	factorization(d);
	backtrack(0,1);
	
	ll q;
	cin >> q;

	//cout << prime_factors.size() << endl;

	while(q--){
		ll u,v;
		cin >> u >> v;
		ll gcd = __gcd(u,v);

		auto one = prime_factors[u];
		auto two = prime_factors[gcd];
		
		ll tot = 0;
		assert(one.size() == two.size());
		for(int i = 0; i < one.size(); i++){
			tot += (one[i].second - two[i].second);
		}
		ll ans = factorial[tot];
		for(int i = 0; i < one.size(); i++){
			ans *= inv[(one[i].second - two[i].second)];
			ans %= MOD;
		}

		one = prime_factors[v];
		//two = prime_factors[gcd];
		
		tot = 0;
		assert(one.size() == two.size());
		for(int i = 0; i < one.size(); i++){
			tot += (one[i].second - two[i].second);
		}
		ans = (ans * factorial[tot]) % MOD;
		for(int i = 0; i < one.size(); i++){
			ans *= inv[(one[i].second - two[i].second)] ;
			ans %= MOD;
		}
		cout << ans << '\n';
	}

		
	return 0;
}