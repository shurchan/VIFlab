/*=====================
 -- Pixl --
 
 Created for CodeCanyon
 by FV iMAGINATION
 =====================*/


#import "_CLImageEditorViewController.h"
#import "CLImageToolBase.h"



@interface _CLImageEditorViewController()
<
CLImageToolProtocol
>
@property (nonatomic, strong) CLImageToolBase *currentTool;
@property (nonatomic, strong, readwrite) CLImageToolInfo *toolInfo;
@property (nonatomic, strong) UIImageView *targetImageView;
@end


@implementation _CLImageEditorViewController
{
    UIImage *_originalImage;
    UIView *_bgView;
}
@synthesize toolInfo = _toolInfo;

- (id)initWithNibName:(NSString *)nibNameOrNil bundle:(NSBundle *)nibBundleOrNil
{
    self = [super initWithNibName:nibNameOrNil bundle:nibBundleOrNil];
    if (self) {
        // Custom initialization
    }
    return self;
}

- (id)init
{
    self = [self initWithNibName:@"_CLImageEditorViewController" bundle:nil];
    if (self){
        self.toolInfo = [CLImageToolInfo toolInfoForToolClass:[self class]];
    }
    return self;
}

- (id)initWithImage:(UIImage *)image
{
    return [self initWithImage:image delegate:nil];
}

- (id)initWithImage:(UIImage*)image delegate:(id<CLImageEditorDelegate>)delegate
{
    self = [self init];
    if (self){
        _originalImage = [image deepCopy];
        self.delegate = delegate;
    }
    return self;
}

- (id)initWithDelegate:(id<CLImageEditorDelegate>)delegate
{
    self = [self init];
    if (self){
        self.delegate = delegate;
    }
    return self;
}



- (void)viewWillAppear:(BOOL)animated {
    
    [self resetZoomScaleWithAnimated:true];
    [self resetImageViewFrame];
    
    
    if (self.targetImageView){
        [self expropriateImageView];
        
    } else {
        [self refreshImageView];
    }
    
    
    // Sets the Title's font and color
    _navigationBar.titleTextAttributes =   [NSDictionary dictionaryWithObjectsAndKeys:
                                            [UIColor whiteColor], NSForegroundColorAttributeName,
                                            [UIFont fontWithName:@"HelveticaNeue-Light" size:17], NSFontAttributeName,nil];
    
    
    // Init ad banners
    [self initiAdBanner];
    [self initAdMobBanner];
}

- (void)viewDidLoad
{
    [super viewDidLoad];
    
    self.title = self.toolInfo.title;
    
    [self resetImageViewFrame];
    
    self.view.frame = [UIScreen mainScreen].bounds;
    
    if([self respondsToSelector:@selector(automaticallyAdjustsScrollViewInsets)]){
        self.automaticallyAdjustsScrollViewInsets = NO;
    }
    
    if([self.navigationController respondsToSelector:@selector(interactivePopGestureRecognizer)]){
        self.navigationController.interactivePopGestureRecognizer.enabled = NO;
    }
    
    if(self.navigationController!=nil){
        [self.navigationController setNavigationBarHidden:false animated:true];
        _navigationBar.hidden = true;
        [_navigationBar popNavigationItemAnimated:false];
    } else {
        _navigationBar.topItem.title = self.title;
    }
    
    [self setMenuView];
    
    if(_imageView==nil){
        _imageView = [UIImageView new];
        [_scrollView addSubview:_imageView];
        //[self refreshImageView];
    }
}




#pragma mark- View transition

- (void)copyImageViewInfo:(UIImageView*)fromView toView:(UIImageView*)toView
{
    CGAffineTransform transform = fromView.transform;
    fromView.transform = CGAffineTransformIdentity;
    
    toView.transform = CGAffineTransformIdentity;
    toView.frame = [toView.superview convertRect:fromView.frame fromView:fromView.superview];
    toView.transform = transform;
    toView.image = fromView.image;
    toView.contentMode = fromView.contentMode;
    toView.clipsToBounds = fromView.clipsToBounds;
    
    fromView.transform = transform;
}


- (void)expropriateImageView
{
    UIWindow *window = [[[UIApplication sharedApplication] delegate] window];
    
    UIImageView *animateView = [UIImageView new];
    [window addSubview:animateView];
    [self copyImageViewInfo:self.targetImageView toView:animateView];
    
    _bgView = [[UIView alloc] initWithFrame:self.view.bounds];
    [self.view insertSubview:_bgView atIndex:0];
    
    _bgView.backgroundColor = self.view.backgroundColor;
    self.view.backgroundColor = [self.view.backgroundColor colorWithAlphaComponent:0];
    
    self.targetImageView.hidden = YES;
    _imageView.hidden = YES;
    _bgView.alpha = 0;
    _navigationBar.transform = CGAffineTransformMakeTranslation(0, -_navigationBar.height);
    _menuView.transform = CGAffineTransformMakeTranslation(0, self.view.height-_menuView.top);
    
    [UIView animateWithDuration:kCLImageToolAnimationDuration
                     animations:^{
                         animateView.transform = CGAffineTransformIdentity;
                         
                         CGFloat dy = ([UIDevice iosVersion]<7) ? [UIApplication sharedApplication].statusBarFrame.size.height : 0;
                         
                         CGSize size = (_imageView.image) ? _imageView.image.size : _imageView.frame.size;
                         if(size.width>0 && size.height>0){
                             CGFloat ratio = MIN(_scrollView.width / size.width, _scrollView.height / size.height);
                             CGFloat W = ratio * size.width;
                             CGFloat H = ratio * size.height;
                             animateView.frame = CGRectMake((_scrollView.width-W)/2 + _scrollView.left, (_scrollView.height-H)/2 + _scrollView.top + dy, W, H);
                         }
                         
                         _bgView.alpha = 1;
                         _navigationBar.transform = CGAffineTransformIdentity;
                         _menuView.transform = CGAffineTransformIdentity;
                     }
                     completion:^(BOOL finished) {
                         self.targetImageView.hidden = NO;
                         _imageView.hidden = NO;
                         [animateView removeFromSuperview];
                         
                     }];
}

- (void)restoreImageView:(BOOL)canceled
{
    if(!canceled){
        self.targetImageView.image = _imageView.image;
    }
    self.targetImageView.hidden = true;
    
    id<CLImageEditorTransitionDelegate> delegate = [self transitionDelegate];
    if([delegate respondsToSelector:@selector(imageEditor:willDismissWithImageView:canceled:)]){
        [delegate imageEditor:self willDismissWithImageView:self.targetImageView canceled:canceled];
    }
    
    UIWindow *window = [[[UIApplication sharedApplication] delegate] window];
    
    UIImageView *animateView = [UIImageView new];
    [window addSubview:animateView];
    [self copyImageViewInfo:_imageView toView:animateView];
    
    _menuView.frame = [window convertRect:_menuView.frame fromView:_menuView.superview];
    _navigationBar.frame = [window convertRect:_navigationBar.frame fromView:_navigationBar.superview];
    
    [window addSubview:_menuView];
    [window addSubview:_navigationBar];
    
    self.view.userInteractionEnabled = NO;
    _menuView.userInteractionEnabled = NO;
    _navigationBar.userInteractionEnabled = NO;
    _imageView.hidden = YES;
    
    [UIView animateWithDuration:0.3
                     animations:^{
                         _bgView.alpha = 0;
                         _menuView.alpha = 0;
                         _navigationBar.alpha = 0;
                         
                         _menuView.transform = CGAffineTransformMakeTranslation(0, self.view.height-_menuView.top);
                         _navigationBar.transform = CGAffineTransformMakeTranslation(0, -_navigationBar.height);
                         
                         [self copyImageViewInfo:self.targetImageView toView:animateView];
                     }
                     completion:^(BOOL finished) {
                         [animateView removeFromSuperview];
                         [_menuView removeFromSuperview];
                         [_navigationBar removeFromSuperview];
                         
                         [self willMoveToParentViewController:nil];
                         [self.view removeFromSuperview];
                         [self removeFromParentViewController];
                         
                         _imageView.hidden = NO;
                         self.targetImageView.hidden = NO;
                         
                         if([delegate respondsToSelector:@selector(imageEditor:didDismissWithImageView:canceled:)]){
                             [delegate imageEditor:self didDismissWithImageView:self.targetImageView canceled:canceled];
                             
                             
                         }
                     }
     ];
}

#pragma mark- Properties

- (id<CLImageEditorTransitionDelegate>)transitionDelegate
{
    if([self.delegate conformsToProtocol:@protocol(CLImageEditorTransitionDelegate)]){
        return (id<CLImageEditorTransitionDelegate>)self.delegate;
    }
    return nil;
}

- (void)setTitle:(NSString *)title
{
    [super setTitle:title];
    _toolInfo.title = title;
}

#pragma mark- ImageTool setting

+ (NSString*)defaultIconImagePath
{
    return nil;
}

+ (CGFloat)defaultDockedNumber
{
    return 0;
}

// Set the Title of the App ==========
+ (NSString*)defaultTitle
{
    return @"Editor";
    
}

+ (BOOL)isAvailable
{
    return true;
}

+ (NSArray*)subtools
{
    return [CLImageToolInfo toolsWithToolClass:[CLImageToolBase class]];
}

+ (NSDictionary*)optionalInfo
{
    return nil;
}




#pragma mark - SET MENU VIEW =======================

- (void)setMenuView
{
    CGFloat x = 0;
    CGFloat W = 70;
    CGFloat H = _menuView.height;
    
    for(CLImageToolInfo *info in _toolInfo.sortedSubtools){
        if(!info.available){
            continue;
        }
        
        CLToolbarMenuItem *view = [CLImageEditorTheme menuItemWithFrame:CGRectMake(x, 0, W, H) target:self action:@selector(tappedMenuView:) toolInfo:info];
        
        [_menuView addSubview:view];
        x += W;
    }
    _menuView.contentSize = CGSizeMake(MAX(x, _menuView.frame.size.width+1), 0);
}

- (void)resetImageViewFrame  {
    
    CGSize size = (_imageView.image) ? _imageView.image.size : _imageView.frame.size;
    NSLog(@"size: %f - %f", size.width, size.height);
    
    if(size.width > 0   &&   size.height > 0) {
        CGFloat ratio = MIN(_scrollView.frame.size.width / size.width, _scrollView.frame.size.height / size.height);
        CGFloat W = ratio * size.width * _scrollView.zoomScale;
        CGFloat H = ratio * size.height * _scrollView.zoomScale;
        _imageView.frame = CGRectMake((_scrollView.width-W)/2, (_scrollView.height-H)/2, W, H);
    }
    
    _scrollView.autoresizingMask = (UIViewAutoresizingFlexibleWidth | UIViewAutoresizingFlexibleHeight | UIViewAutoresizingFlexibleBottomMargin );
    
    NSLog(@"ImageVIEW: %f -- %f", _imageView.frame.size.width, _imageView.frame.size.height);
    NSLog(@"UIImage: %f -- %f", _imageView.image.size.width, _imageView.image.size.height);
    NSLog(@"scrollView: %f - %f", _scrollView.frame.size.width, _scrollView.frame.size.height);
    
}

- (void)fixZoomScaleWithAnimated:(BOOL)animated
{
    CGFloat minZoomScale = _scrollView.minimumZoomScale;
    _scrollView.maximumZoomScale = 0.95*minZoomScale;
    _scrollView.minimumZoomScale = 0.95*minZoomScale;
    [_scrollView setZoomScale:_scrollView.minimumZoomScale animated:animated];
}

- (void)resetZoomScaleWithAnimated:(BOOL)animated
{
    NSLog(@"resetZoomScaleWithAnimated");
    _scrollView.zoomScale = 1;
}

- (void)refreshImageView
{
    _imageView.image = _originalImage;
    
    [self resetImageViewFrame];
}

- (UIBarPosition)positionForBar:(id <UIBarPositioning>)bar
{
    return UIBarPositionTopAttached;
}

- (BOOL)shouldAutorotate
{
    return false;
}

- (NSUInteger)supportedInterfaceOrientations
{
    return UIInterfaceOrientationMaskPortrait;
}



#pragma mark- TOOL ACTIONS ===============
- (void)setCurrentTool:(CLImageToolBase *)currentTool
{
    if (currentTool != _currentTool){
        [_currentTool cleanup];
        _currentTool = currentTool;
        [_currentTool setup];
        
        [self swapToolBarWithEditting:(_currentTool!=nil)];
    }
}



#pragma mark- MENU ACTIONS ==================
- (void)swapMenuViewWithEditting:(BOOL)editting
{
    [UIView animateWithDuration:kCLImageToolAnimationDuration animations:^{
        if (editting){
            _menuView.transform = CGAffineTransformMakeTranslation(0, self.view.height - _menuView.top);
        } else {
            _menuView.transform = CGAffineTransformIdentity;
        }
    }];
}

- (void)swapNavigationBarWithEditting:(BOOL)editting
{
    if(self.navigationController == nil){
        return;
    }
    
    [self.navigationController setNavigationBarHidden:editting animated:true];
    
    if (editting) {
        
        _navigationBar.hidden = NO;
        _navigationBar.transform = CGAffineTransformMakeTranslation(0, -_navigationBar.height);
        
        [UIView animateWithDuration:kCLImageToolAnimationDuration animations:^{
         _navigationBar.transform = CGAffineTransformIdentity;
        }];
        
    } else {
        
        [UIView animateWithDuration:kCLImageToolAnimationDuration animations:^{
        _navigationBar.transform = CGAffineTransformMakeTranslation(0, -_navigationBar.height);
        } completion:^(BOOL finished) {
        _navigationBar.hidden = YES;
        _navigationBar.transform = CGAffineTransformIdentity;
        }];
    }
}

- (void)swapToolBarWithEditting:(BOOL)editting
{
    [self swapMenuViewWithEditting:editting];
    [self swapNavigationBarWithEditting:editting];
    
    if (self.currentTool){
        
        UINavigationItem *item  = [[UINavigationItem alloc] initWithTitle:self.currentTool.toolInfo.title];
        
        item.rightBarButtonItem = [[UIBarButtonItem alloc] initWithTitle:NSLocalizedStringWithDefaultValue(@"CLImageEditor_OKBtnTitle", nil, [CLImageEditorTheme bundle], @"OK", @"") style:UIBarButtonItemStyleDone target:self action:@selector(pushedDoneBtn:)];
        
        item.leftBarButtonItem  = [[UIBarButtonItem alloc] initWithTitle:NSLocalizedStringWithDefaultValue(@"CLImageEditor_BackBtnTitle", nil, [CLImageEditorTheme bundle], @"Back", @"") style:UIBarButtonItemStylePlain target:self action:@selector(pushedCancelBtn:)];
        
        [_navigationBar pushNavigationItem:item animated:(self.navigationController==nil)];
        
    } else {
        [_navigationBar popNavigationItemAnimated:(self.navigationController==nil)];
    }
}

- (void)setupToolWithToolInfo:(CLImageToolInfo*)info
{
    if(self.currentTool){ return; }
    
    Class toolClass = NSClassFromString(info.toolName);
    
    if(toolClass){
        id instance = [toolClass alloc];
        if(instance!=nil && [instance isKindOfClass:[CLImageToolBase class]]){
            instance = [instance initWithImageEditor:self withToolInfo:info];
            self.currentTool = instance;
        }
    }
}

- (void)tappedMenuView:(UITapGestureRecognizer*)sender
{
    UIView *view = sender.view;
    
    view.alpha = 0.2;
    [UIView animateWithDuration:kCLImageToolAnimationDuration animations:^{
       view.alpha = 1;
    }];
    
    [self setupToolWithToolInfo:view.toolInfo];
    
}



#pragma mark - CANCEL BUTTON METHOD ===================
- (IBAction)pushedCancelBtn:(id)sender
{
    _imageView.image = _originalImage;
    [self resetImageViewFrame];
    
    self.currentTool = nil;
}

#pragma mark - DONE BUTTON METHOD ======================
- (IBAction)pushedDoneBtn:(id)sender
{
    self.view.userInteractionEnabled = NO;
    
    [self.currentTool executeWithCompletionBlock:^(UIImage *image, NSError *error, NSDictionary *userInfo) {
        if(error){
            UIAlertView *alert = [[UIAlertView alloc] initWithTitle:@"Error" message:error.localizedDescription delegate:nil cancelButtonTitle:@"OK" otherButtonTitles:nil];
            [alert show];
        }
        else if(image){
            _originalImage = image;
            _imageView.image = image;
            
            [self resetImageViewFrame];
            self.currentTool = nil;
        }
        self.view.userInteractionEnabled = true;
    }];
}



- (void)pushedCloseBtn:(id)sender  {
    if (self.targetImageView==nil){
        if([self.delegate respondsToSelector:@selector(imageEditorDidCancel:)]){
            [self.delegate imageEditorDidCancel:self];
            
        } else {
            [self dismissViewControllerAnimated:true completion:nil];
        }
        
    } else {
        _imageView.image = _targetImageView.image;
        [self restoreImageView:true];
    }
}

- (void)pushedFinishBtn:(id)sender
{
    if(self.targetImageView==nil){
        if([self.delegate respondsToSelector:@selector(imageEditor:didFinishEdittingWithImage:)]){
            [self.delegate imageEditor:self didFinishEdittingWithImage:_originalImage];
            
        } else {
            
            [self dismissViewControllerAnimated:true completion:nil];
        }
        
    } else {
        _imageView.image = _originalImage;
        [self restoreImageView:NO];
    }
}

#pragma mark- ScrollView delegate ============================

- (UIView *)viewForZoomingInScrollView:(UIScrollView *)scrollView
{
    return _imageView;
}

- (void)scrollViewDidZoom:(UIScrollView *)scrollView
{
    CGFloat Ws = _scrollView.frame.size.width - _scrollView.contentInset.left - _scrollView.contentInset.right;
    CGFloat Hs = _scrollView.frame.size.height - _scrollView.contentInset.top - _scrollView.contentInset.bottom;
    CGFloat W = _imageView.frame.size.width;
    CGFloat H = _imageView.frame.size.height;
    
    CGRect rct = _imageView.frame;
    rct.origin.x = MAX((Ws-W)/2, 0);
    rct.origin.y = MAX((Hs-H)/2, 0);
    _imageView.frame = rct;
}







#pragma mark - iAd + AdMob BANNER METHODS ===========================

// Initialize Apple iAd banner
-(void)initiAdBanner {
    if (!_iAdBannerView) {
        CGRect rect = CGRectMake(0, self.view.frame.size.height, 0, 0);
        _iAdBannerView = [[ADBannerView alloc]initWithFrame:rect];
        _iAdBannerView.delegate = self;
        _iAdBannerView.hidden = true;
        [self.view addSubview: _iAdBannerView];
    }
}

// Initialize Google AdMob banner
-(void)initAdMobBanner {
    if (!_adMobBannerView) {
        if ( UI_USER_INTERFACE_IDIOM() == UIUserInterfaceIdiomPad )  {
            // iPad banner
            CGRect rect = CGRectMake(0, self.view.frame.size.height, GAD_SIZE_728x90.width, GAD_SIZE_728x90.height);
            _adMobBannerView = [[GADBannerView alloc] initWithFrame:rect];
        } else {
            // iPhone banner
            CGRect rect = CGRectMake(0, self.view.frame.size.height, GAD_SIZE_320x50.width, GAD_SIZE_320x50.height);
            _adMobBannerView = [[GADBannerView alloc] initWithFrame:rect];
        }
    }
    
    /*=== IMPORTANT: REPLACE THE RED STRING BELOW WITH THE UNIT ID YOU'VE GOT
     BY REGISTERING YOUR APP IN www.apps.admob.com  ===*/
    _adMobBannerView.adUnitID = @"ca-app-pub-3940256099942544/2934735716";
    //========================================================================
    
    _adMobBannerView.rootViewController = self;
    _adMobBannerView.delegate = self;
    _adMobBannerView.hidden = true;
    [self.view addSubview: _adMobBannerView];
}


// Hide the banner by sliding down
-(void)hideBanner:(UIView *)banner {
    if (banner && !banner.isHidden) {
        [UIView beginAnimations:@"hideBanner" context:nil];
        
        // Hide the banner moving it below the bottom of the screen
        banner.frame = CGRectOffset(banner.frame, 0, banner.frame.size.height);
        
        [UIView commitAnimations];
        banner.hidden = true;
    }
}

// Show the banner by sliding up
-(void)showBanner:(UIView *)banner {
    if (banner && banner.isHidden) {
        [UIView beginAnimations:@"showBanner" context:nil];
        
        // Place the banner on the bottom of the screen
        banner.frame = CGRectMake(0, self.view.frame.size.height - banner.frame.size.height, banner.frame.size.width, banner.frame.size.height);
        
        // *Uncomment this line to place the banner 44px underneath the top of the screen (and comment the line above)*
        // banner.frame = CGRectMake(0, 44, banner.frame.size.width, banner.frame.size.height);
        
        [UIView commitAnimations];
        banner.hidden = false;
    }
}

// Called before the add is shown, time to move the view
- (void)bannerViewWillLoadAd:(ADBannerView *)banner {
    NSLog(@"iAd load");
    [self hideBanner: _adMobBannerView];
    [self showBanner: _iAdBannerView];
}

// Called when an error occured
- (void)bannerView:(ADBannerView *)banner didFailToReceiveAdWithError:(NSError *)error {
    NSLog(@"iAd error: %@", error);
    [self hideBanner: _iAdBannerView];
    [_adMobBannerView loadRequest:[GADRequest request]];
}

// Called before ad is shown, good time to show the add
- (void)adViewDidReceiveAd:(GADBannerView *)view {
    NSLog(@"Admob load");
    [self hideBanner: _iAdBannerView];
    [self showBanner: _adMobBannerView];
}

// An error occured
- (void)adView:(GADBannerView *)view didFailToReceiveAdWithError:(GADRequestError *)error {
    NSLog(@"Admob error: %@", error);
    [self hideBanner: _adMobBannerView];
}






- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
}

@end
